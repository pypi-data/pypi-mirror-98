"""
    lager.status

    Job status output functions
"""
try:
    _TERMIOS_IMPORT_FAILED = False
    import termios
    import tty
except (ImportError, ModuleNotFoundError) as exc:
    _TERMIOS_IMPORT_FAILED = exc
import platform
import threading
import sys
import os
import select
from functools import partial
import bson
import click
import trio
import lager_trio_websocket as trio_websocket
from lager_trio_websocket import open_websocket_url
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import wsproto.frame_protocol as wsframeproto
import requests
from .matchers import test_matcher_factory
from .util import heartbeat

def stream_response(response):
    """
        Stream a ``requests`` response to the terminal
    """
    with response:
        for chunk in response.iter_content(chunk_size=None):
            click.echo(chunk, nl=False)

async def handle_url_message(matcher, urls):
    """
        Handle a message with data location urls
    """
    downloader = partial(requests.get, stream=True)
    for url in urls:
        response = await trio.to_thread.run_sync(downloader, url)
        response.raise_for_status()
        await trio.to_thread.run_sync(stream_response, response)

async def handle_data_message(matcher, message):
    """
        Handle a data message
    """
    for item in message:
        entry = item['entry']
        if 'payload' in entry:
            payload = entry['payload']
            matcher.feed(payload)

async def handle_message(matcher, message):
    """
        Handle an individual parsed websocket message
    """
    if 'data' in message:
        return await handle_data_message(matcher, message['data'])
    if 'urls' in message:
        return await handle_url_message(matcher, message['urls'])
    return None

class InterMessageTimeout(Exception):
    """
        Raised if no messages received for ``message_timeout`` seconds
    """
    pass

async def read_from_websocket(websocket, matcher, message_timeout, nursery):
    try:
        while True:
            try:
                with trio.fail_after(message_timeout):
                    try:
                        message = await websocket.get_message()
                    except trio_websocket.ConnectionClosed as exc:
                        if exc.reason is None:
                            return
                        if exc.reason.code != wsframeproto.CloseReason.NORMAL_CLOSURE or exc.reason.reason != 'EOF':
                            raise
                        break
            except trio.TooSlowError:
                raise InterMessageTimeout(message_timeout)
            await handle_message(matcher, bson.loads(message))
    finally:
        matcher.done()
        nursery.cancel_scope.cancel()

def reader_function(io, send_channel, trio_token):
    try:
        while True:
            data = io.read()
            if data is not None:
                trio.from_thread.run(send_channel.send, {'type': 'data', 'value': data}, trio_token=trio_token)
    except EOFError:
        trio.from_thread.run(send_channel.send, {'type': 'EOF'}, trio_token=trio_token)
    except KeyboardInterrupt:
        trio.from_thread.run(send_channel.send, {'type': 'Ctrl+C'}, trio_token=trio_token)


async def write_to_websocket(websocket, receive_channel, eof_timeout, nursery):
    while True:
        message = await receive_channel.receive()
        if message['type'] == 'EOF':
            if eof_timeout is not None:
                await trio.sleep(eof_timeout)
                await websocket.aclose()
            return

        if message['type'] == 'Ctrl+C':
            raise KeyboardInterrupt

        if message['type'] == 'data':
            data = message['value']
            try:
                await websocket.send_message(data)
            except trio_websocket.ConnectionClosed as exc:
                if exc.reason is None:
                    return
                if exc.reason.code != wsframeproto.CloseReason.NORMAL_CLOSURE or exc.reason.reason != 'EOF':
                    raise
                return

class TTYIO:
    """
        Class for doing I/O with a TTY managed by curses
    """
    def __init__(self, line_ending=b'', opost=False):
        self.stdin_fileno = sys.stdin.fileno()
        self.stdout_fileno = sys.stdout.fileno()
        self.old_settings = termios.tcgetattr(self.stdin_fileno)
        tty.setraw(self.stdin_fileno)
        self.line_ending = line_ending
        self._opost = opost

    def shutdown(self):
        """
            Restore previous TTY settings
        """
        self.restore()

    def restore(self):
        termios.tcsetattr(self.stdin_fileno, termios.TCSADRAIN, self.old_settings)

    def output(self, data, fg=None, flush=False):
        """
            Output some data to the TTY
        """
        if self._opost:
            self.restore()
            if fg:
                click.secho(data, nl=False, fg=fg)
            else:
                click.echo(data, nl=False)
            if flush:
                sys.stdout.flush()

            tty.setraw(self.stdin_fileno)
        else:
            os.write(self.stdout_fileno, data)

    def read(self):
        """
            Read a key from the TTY
        """
        char = os.read(self.stdin_fileno, 1)
        if char == b'':
            raise EOFError
        if char == b'\x03':
            raise KeyboardInterrupt

        if char == b'\r':
            return self.line_ending or char
        return char

class StandardIO:
    """
        Class for doing I/O with standard UNIX io streams
    """
    def shutdown(self):
        """
            No special behavior needed
        """
        pass

    def output(self, data, fg=None, flush=False):
        """
            Send some data to stdout
        """
        if fg:
            click.secho(data, nl=False, fg=fg)
        else:
            click.echo(data, nl=False)
        if flush:
            sys.stdout.flush()

    def read(self):
        """
            Read some data from stdin
        """
        rlist, _wlist, xlist = select.select([sys.stdin], [], [sys.stdin])
        if rlist:
            chunk = sys.stdin.buffer.read()
            if chunk == b'':
                raise EOFError
            return chunk
        if xlist:
            raise EOFError
        return None


@retry(reraise=True, sleep=trio.sleep, stop=stop_after_attempt(4), wait=wait_fixed(2), retry=retry_if_exception_type(trio_websocket.ConnectionRejected))
async def display_job_output(connection_params, test_runner, interactive, line_ending, message_timeout, overall_timeout, eof_timeout, success_regex=None, failure_regex=None, opost=False):
    """
        Display job output from websocket
    """
    (uri, kwargs) = connection_params
    match_class = test_matcher_factory(test_runner)
    if interactive:
        io_source = TTYIO(line_ending, opost)
    else:
        io_source = StandardIO()
    try:
        matcher = match_class(io_source, success_regex, failure_regex)
        send_channel, receive_channel = trio.open_memory_channel(0)
        allow_reader = True
        if platform.system() == 'Windows' and not interactive:
            allow_reader = False
        with trio.fail_after(overall_timeout):
            async with open_websocket_url(uri, disconnect_timeout=1, **kwargs) as websocket:
                if allow_reader:
                    token = trio.lowlevel.current_trio_token()
                    thread = threading.Thread(target=reader_function, args=(io_source, send_channel, token), daemon=True)
                    thread.start()
                async with trio.open_nursery() as nursery:
                    nursery.start_soon(heartbeat, websocket, 30, 30)
                    nursery.start_soon(read_from_websocket, websocket, matcher, message_timeout, nursery)
                    nursery.start_soon(write_to_websocket, websocket, receive_channel, eof_timeout, nursery)
        return matcher
    finally:
        if io_source:
            io_source.shutdown()

def run_job_output(connection_params, test_runner, interactive, line_ending, message_timeout, overall_timeout, eof_timeout, debug=False, success_regex=None, failure_regex=None, opost=False):
    """
        Run async task to get job output from websocket
    """
    if interactive and _TERMIOS_IMPORT_FAILED:
        click.echo(_TERMIOS_IMPORT_FAILED, err=True)
        click.echo('Interactive terminal not currently supported by Windows; please try running in Docker.', err=True)
        click.get_current_context().exit(1)

    if not line_ending:
        line_ending = b''
    elif line_ending == 'LF':
        line_ending = b'\n'
    elif line_ending == 'CRLF':
        line_ending = b'\r\n'
    else:
        raise ValueError('Invalid line ending')

    try:
        matcher = trio.run(display_job_output, connection_params, test_runner, interactive, line_ending, message_timeout, overall_timeout, eof_timeout, success_regex, failure_regex, opost)
        click.get_current_context().exit(matcher.exit_code)
    except trio.TooSlowError:
        suffix = '' if overall_timeout == 1 else 's'
        message = f'Job status timed out after {overall_timeout} second{suffix}'
        click.secho(message, fg='red', err=True)
        click.get_current_context().exit(1)
    except InterMessageTimeout:
        suffix = '' if message_timeout == 1 else 's'
        message = f'Timed out after no messages received for {message_timeout} second{suffix}'
        click.secho(message, fg='red', err=True)
        click.get_current_context().exit(1)
    except requests.exceptions.HTTPError as exc:
        response = getattr(exc, 'response')
        if response is not None and response.status_code == 404:
            click.secho('Test run content not found', fg='red', err=True)
        else:
            click.secho('Error retrieving test run content', fg='red', err=True)
        if debug:
            raise
    except trio_websocket.ConnectionRejected as exc:
        if exc.status_code == 404:
            click.secho('Job not found', fg='red', err=True)
        elif exc.status_code >= 500:
            click.secho('Internal error in Lager API. '
                        'Please contact support@lagerdata.com if this persists.',
                        fg='red', err=True)
        else:
            click.secho('Could not connect to API websocket', fg='red', err=True)
        if debug:
            raise
        click.get_current_context().exit(1)
    except trio_websocket.HandshakeError as exc:
        click.secho('Could not connect to API websocket', fg='red', err=True)
        if debug:
            raise
        click.get_current_context().exit(1)
    except trio_websocket.ConnectionClosed as exc:
        if exc.reason.code != wsframeproto.CloseReason.NORMAL_CLOSURE:
            click.secho('API websocket closed abnormally', fg='red', err=True)
            if debug:
                raise
            click.get_current_context().exit(1)
        elif exc.reason.reason != 'EOF':
            click.secho('API websocket closed unexpectedly', fg='red', err=True)
            if debug:
                raise
            click.get_current_context().exit(1)
    except ConnectionRefusedError:
        click.secho('Lager API websocket connection refused!', fg='red', err=True)
        if debug:
            raise
        click.get_current_context().exit(1)
