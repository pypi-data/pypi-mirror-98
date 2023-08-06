import time
import asyncio
import argparse
import tempfile
import traceback
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import asyncssh

from .run import run
from .colors import ColorMode, detect_color_mode
from .file_input import gb_input_from_file_context
from .keyboard_input import gb_input_from_keyboard_context
from .main import add_base_arguments, add_optional_arguments

from .ssh_app_session import process_to_app_session


async def detect_true_color_support(process, timeout=0.5):
    # Disable line mode
    process.channel.set_line_mode(False)
    # Set unlikely RGB value
    process.stdout.write("\033[48:2:1:2:3m")
    # Query current configuration
    process.stdout.write("\033P$qm\033\\")
    # Reset
    process.stdout.write("\033[m")
    # Wait for reply
    while True:
        try:
            header = await asyncio.wait_for(process.stdin.readuntil("\033\\"), timeout)
        except asyncssh.TerminalSizeChanged:
            pass
        except asyncio.TimeoutError:
            return False
        else:
            break
    # Return whether true color is supported
    return "P1$r" in header and "48:2" in header and "1:2:3m" in header


async def safe_ssh_process_handler(process):
    try:
        result = await ssh_process_handler(process)
    except KeyboardInterrupt:
        result = 1
    except SystemExit as e:
        result = e.code or 0
    except BaseException:
        traceback.print_exc()
        result = 1
    return process.exit(result or 0)


async def ssh_process_handler(process):
    executor = process.get_extra_info("executor")
    app_config = process.get_extra_info("app_config")
    display = process.channel.get_x11_display()
    command = process.channel.get_command()
    environment = process.channel.get_environment()
    terminal_type = process.get_terminal_type()
    connection = process.get_extra_info("connection")
    username = process.get_extra_info("username")
    peername, port = connection.get_extra_info("peername")
    print(f"> User `{username}` is connected ({peername}:{port})")

    # Check command
    if command is not None:
        parser = argparse.ArgumentParser()
        parser._print_message = lambda message, file=None: type(parser)._print_message(
            parser, message, file=process.stdout
        )
        add_optional_arguments(parser)
        parser.parse_args(command.split(), app_config)

    # Check terminal
    if terminal_type is None:
        print(
            "Please use a terminal to access the interactive interface.",
            "Use `-t` to force pseudo-terminal allocation if a command is provided.",
            sep="\n",
            file=process.stdout,
        )
        print(f"< User `{username}` did not use an interactive terminal")
        return 1

    # X11 is required
    if not display and app_config.input_file is None:
        print(
            """\
X11 forwarding is required and can be enabled using the `-X` option.

===============================[ WARNING ]=====================================
Enabling X11 forwarding while connecting to an untrusted server can greatly
endanger your machine. Please only do so if you are running the X11 server in a
sandbox. More information here: https://security.stackexchange.com/a/7496
===============================[ WARNING ]=====================================""",
            file=process.stdout,
        )
        print(f"< User `{username}` did not enable X11 forwarding")
        return 1

    # Detect true color support by interracting with the terminal
    if app_config.color_mode is not None:
        color_mode = app_config.color_mode
    elif await detect_true_color_support(process):
        color_mode = ColorMode.HAS_24_BIT_COLOR
    else:
        environment["TERM"] = terminal_type
        color_mode = detect_color_mode(environment)

    if color_mode == ColorMode.NO_COLOR:
        print(
            "Your terminal `{terminal_type}` doesn't seem to support colors.",
            file=process.stdout,
        )
        print(f"< User `{username}`terminal `{terminal_type}` does not support colors")
        return 1

    async with process_to_app_session(process) as app_session:
        loop = asyncio.get_event_loop()
        height, width = app_session.output.get_size()
        print(
            f"[Terminal Info] {username}: {terminal_type}, {color_mode}, {width}x{height}"
        )
        await loop.run_in_executor(
            executor,
            thread_target,
            app_session,
            app_config,
            username,
            display,
            color_mode,
        )


def thread_target(app_session, app_config, username, display, color_mode):
    if app_config.input_file is not None:
        gb_input_context = gb_input_from_file_context(
            app_config.input_file, app_config.skip_inputs
        )
        save_directory = tempfile.mkdtemp()
    else:
        gb_input_context = gb_input_from_keyboard_context(display=display)
        save_directory = Path("ssh_save") / username
        save_directory.mkdir(parents=True, exist_ok=True)

    with gb_input_context as get_gb_input:
        try:
            # Prepare alternate screen
            app_session.output.enter_alternate_screen()
            app_session.output.erase_screen()
            app_session.output.hide_cursor()
            app_session.output.flush()

            # Run the emulator
            return_code = run(
                romfile=app_config.romfile,
                get_input=get_gb_input,
                app_session=app_session,
                frame_advance=app_config.frame_advance,
                color_mode=color_mode,
                break_after=app_config.break_after,
                speed_factor=app_config.speed_factor,
                use_cpr_sync=app_config.cpr_sync,
                save_directory=str(save_directory),
                force_gameboy=app_config.force_gameboy,
            )
        except (KeyboardInterrupt, OSError):
            return 0
        else:
            return return_code
        finally:
            # Wait for CPR
            time.sleep(0.1)
            # Clear alternate screen
            app_session.input.read_keys()
            app_session.output.erase_screen()
            app_session.output.quit_alternate_screen()
            app_session.output.show_cursor()
            # Flush if the connection is still active
            try:
                app_session.output.flush()
            except BrokenPipeError:
                pass


class SSHServer(asyncssh.SSHServer):
    def __init__(self, app_config, executor):
        self._app_config = app_config
        self._executor = executor

    def connection_made(self, conn):
        conn.set_extra_info(executor=self._executor)
        conn.set_extra_info(app_config=self._app_config)

    def begin_auth(self, username):
        return True

    def session_requested(self):
        return asyncssh.SSHServerProcess(safe_ssh_process_handler, None, None)

    def password_auth_supported(self):
        return self._app_config.password

    def validate_password(self, username, password):
        return password == self._app_config.password


async def run_server(app_config, executor):
    user_private_key = str(Path("~/.ssh/id_rsa").expanduser())
    user_public_key = str(Path("~/.ssh/id_rsa.pub").expanduser())

    # Remove chacha20 from encryption_algs because it's a bit too expensive
    encryption_algs = [
        # "chacha20-poly1305@openssh.com",
        "aes256-gcm@openssh.com",
        "aes128-gcm@openssh.com",
        "aes256-ctr",
        "aes192-ctr",
        "aes128-ctr",
    ]

    server = await asyncssh.create_server(
        lambda: SSHServer(app_config, executor),
        app_config.bind,
        app_config.port,
        server_host_keys=[user_private_key],
        authorized_client_keys=user_public_key,
        x11_forwarding=True,
        encryption_algs=encryption_algs,
    )
    bind, port = server.sockets[0].getsockname()
    print(f"Running ssh server on {bind}:{port}...")

    await server.wait_closed()


def main(args=None):
    parser = argparse.ArgumentParser(description="Gambatte terminal front-end over ssh")
    add_base_arguments(parser)
    add_optional_arguments(parser)
    parser.add_argument(
        "--bind",
        "-b",
        type=str,
        default="localhost",
        help="Bind adress of the SSH server, use `0.0.0.0` for all interfaces (default is localhost)",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8022,
        help="Port of the SSH server (default is 8022)",
    )
    parser.add_argument(
        "--password",
        "--pw",
        type=str,
        help="Enable password authentification with the given global password",
    )

    # Parse arguments
    app_config = parser.parse_args(args)

    # Run an executor with no limit on the number of threads
    with ThreadPoolExecutor(max_workers=32) as executor:

        # Run the server in asyncio
        asyncio.run(run_server(app_config, executor))


if __name__ == "__main__":
    main()
