"""
    lager.webcam.commands

    webcam tunnel commands
"""

import click
import trio
from ..gdbserver.tunnel import serve_tunnel
from ..context import get_default_gateway, ensure_debugger_running

def run_webcam_tunnel(ctx, host, port, gateway):
    connection_params = ctx.obj.websocket_connection_params(socktype='webcam-tunnel', gateway_id=gateway)
    try:
        trio.run(serve_tunnel, host, port, connection_params, 'webcam')
    except PermissionError as exc:
        if port < 1024:
            click.secho(f'Permission denied for port {port}. Using a port number less than '
                        '1024 typically requires root privileges.', fg='red', err=True)
        else:
            click.secho(str(exc), fg='red', err=True)
        if ctx.obj.debug:
            raise
    except OSError as exc:
        click.secho(f'Could not start webcam on port {port}: {exc}', fg='red', err=True)
        if ctx.obj.debug:
            raise

@click.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected')
@click.option('--host', default='localhost', help='interface for webcam to bind. '
              'Use --host \'*\' to bind to all interfaces.', show_default=True)
@click.option('--port', default=8081, help='Port for webcam', show_default=True)
def webcam(ctx, gateway, host, port):
    """

    """
    if gateway is None:
        gateway = get_default_gateway(ctx)

    run_webcam_tunnel(ctx, host, port, gateway)
