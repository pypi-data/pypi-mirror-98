import sys
import re
import enum
import click

def test_matcher_factory(test_runner):
    """
        Return matcher for named test_runner
    """
    if test_runner is None or test_runner == 'none':
        return EmptyMatcher
    if test_runner == 'unity':
        return UnityMatcher
    if test_runner.startswith('endswith:'):
        return EndsWithMatcher

    raise ValueError(f'Unknown test matcher {test_runner}')

def echo_line(line, color):
    """
        Try to echo a line with color, otherwise just emit it raw
    """
    try:
        decoded_line = line.decode()
        click.secho(decoded_line, fg=color)
    except UnicodeDecodeError:
        click.echo(line)


class V1ParseStates(enum.Enum):
    """
        Parser states
    """
    Start = 'start'
    FirstSpace = 'first_space'
    Length = 'length'
    SecondSpace = 'second_space'
    Content = 'content'


def iter_streams(response):
    """
        Iterate over file streams returned from python running on the gateway
    """
    parse_state = V1ParseStates.Start
    fileno = None
    data = b''
    length_str = b''
    length = None
    for chunk in response.iter_content(chunk_size=1):
        if parse_state == V1ParseStates.Start:
            if chunk == b'-':
                fileno = -1
            else:
                fileno = int(chunk.decode(), 10)
            parse_state = V1ParseStates.FirstSpace
        elif parse_state == V1ParseStates.FirstSpace:
            parse_state = V1ParseStates.Length
        elif parse_state == V1ParseStates.Length:
            if chunk == b' ':
                length = int(length_str.decode())
                length_str = b''
                if length == 0:
                    parse_state = V1ParseStates.Start
                else:
                    parse_state = V1ParseStates.Content
            else:
                length_str += chunk
        elif V1ParseStates.Content:
            data += chunk
            if len(data) == length:
                yield (fileno, data)
                data = b''
                length = None
                fileno = None
                parse_state = V1ParseStates.Start


class UnityMatcher:
    summary_separator = b'-----------------------'

    def __init__(self, io, _success_regex, _failure_regex):
        self.state = b''
        self.separator = None
        self.has_fail = False
        self.in_summary = False
        self.io = io

    def feed(self, data):
        self.state += data
        if b'\n' not in data:
            return

        lines = self.state.split(b'\n')
        to_process, remainder = lines[:-1], lines[-1]
        self.state = remainder
        for line in to_process:
            if line == self.summary_separator:
                self.in_summary = True
                click.echo(line)
                continue
            if self.in_summary:
                color = 'red' if self.has_fail else 'green'
                echo_line(line, color)
            else:
                if b':FAIL' in line:
                    self.has_fail = True
                    echo_line(line, 'red')
                elif b':PASS' in line:
                    echo_line(line, 'green')
                elif b':INFO' in line:
                    echo_line(line, 'yellow')
                else:
                    click.echo(line)
                sys.stdout.flush()

    def done(self):
        pass

    @property
    def exit_code(self):
        if self.has_fail:
            return 1
        return 0

class EmptyMatcher:
    def __init__(self, io, _success_regex, _failure_regex):
        self.io = io

    def feed(self, data):
        self.io.output(data, flush=True)

    def done(self):
        pass

    @property
    def exit_code(self):
        return 0

def safe_decode(s):
    """
        Try to decode s; if it fails return the escaped string representation
        of the bytes
    """
    try:
        return s.decode()
    except UnicodeDecodeError:
        return str(s).replace("b'", '', 1)[:-1]

class EndsWithMatcher:
    def __init__(self, io, success_regex, failure_regex):
        self.io = io
        self.success_regex = None
        self.failure_regex = None
        if success_regex:
            self.success_regex = re.compile(success_regex.encode())
        if failure_regex:
            self.failure_regex = re.compile(failure_regex.encode())
        self.state = b''
        self._exit_code = 0

    def feed(self, data):
        data = self.state + data
        lines = data.split(b'\n')
        if data.endswith(b'\n'):
            self.state = b''
        else:
            self.state = lines[-1]
            lines = lines[:-1]

        for line in lines:
            color = None
            failed = False
            if self.failure_regex:
                if self.failure_regex.search(line):
                    failed = True
                    color = 'red'
                    self._exit_code = 1
                    line = safe_decode(line)
            if not failed and self.success_regex:
                if self.success_regex.search(line):
                    color = 'green'
                    line = safe_decode(line)

            self.io.output(line, fg=color, flush=False)
            self.io.output(b'\n', flush=True)

    def done(self):
        if self.state:
            self.io.output(self.state)

    @property
    def exit_code(self):
        return self._exit_code
