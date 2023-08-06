#!/usr/bin/env python3

import time
import tempfile
import argparse

from prompt_toolkit.application import create_app_session

from .run import run
from .audio import audio_player, no_audio
from .colors import detect_local_color_mode
from .file_input import gb_input_from_file_context
from .keyboard_input import gb_input_from_keyboard_context
from .controller_input import combine_gb_input_from_controller_context


def add_base_arguments(parser):
    parser.add_argument(
        "romfile", metavar="ROM", type=str, help="Path to a GB or GBC rom file"
    )
    parser.add_argument(
        "--input-file", "-i", default=None, help="Path to a bizhawk BK2 file"
    )
    parser.add_argument(
        "--frame-advance",
        "--fa",
        type=int,
        default=1,
        help="Number of frames to run before displaying the next one (default is 1)",
    )
    parser.add_argument(
        "--break-after",
        "--ba",
        type=int,
        default=None,
        help="Number of frames to run before forcing the emulator to stop (doesn't stop by default)",
    )
    parser.add_argument(
        "--speed-factor",
        "--sf",
        type=float,
        default=1.0,
        help="Speed factor to apply to the emulation (default is 1.0 corresponding to 60 FPS)",
    )
    parser.add_argument(
        "--force-gameboy",
        "--fg",
        action="store_true",
        help="Force the emulator to treat the rom as a GB file",
    )
    parser.add_argument(
        "--skip-inputs",
        "--si",
        type=int,
        default=188,
        help="Number of frame inputs to skip in order to compensate for the lack of BIOS (default is 188)",
    )
    parser.add_argument(
        "--cpr-sync",
        "--cs",
        action="store_true",
        help="Use CPR synchronization to prevent video buffering",
    )
    parser.add_argument(
        "--enable-controller",
        "--ec",
        action="store_true",
        help="Enable game controller support",
    )
    return parser


def main(args=None):
    parser = argparse.ArgumentParser(
        prog="gambaterm", description="Gambatte terminal front-end"
    )
    add_base_arguments(parser)
    parser.add_argument(
        "--disable-audio", "--da", action="store_true", help="Disable audio entirely"
    )
    parser.add_argument(
        "--color-mode",
        "-c",
        type=int,
        default=None,
        help="Force a color mode (1: 4 greyscale colors, 2: 16 colors, 3: 256 colors, 4: 24-bit colors)",
    )
    args = parser.parse_args(args)

    if args.input_file is not None:
        save_directory = tempfile.mkdtemp()
        gb_input_context = gb_input_from_file_context(args.input_file, args.skip_inputs)
    else:
        gb_input_context = gb_input_from_keyboard_context()
        save_directory = None
        if args.enable_controller:
            gb_input_context = combine_gb_input_from_controller_context(
                gb_input_context
            )

    if args.color_mode == 0:
        raise RuntimeError("No color mode seems to be supported")

    # Enter terminal raw mode
    with create_app_session() as app_session:
        with app_session.input.raw_mode():
            try:

                # Detect color mode
                if args.color_mode is None:
                    args.color_mode = detect_local_color_mode(app_session)

                # Prepare alternate screen
                app_session.output.enter_alternate_screen()
                app_session.output.erase_screen()
                app_session.output.hide_cursor()
                app_session.output.flush()

                # Enter input and audio contexts
                with gb_input_context as get_gb_input:
                    player = no_audio if args.disable_audio else audio_player
                    with player(args.speed_factor) as audio_out:

                        # Run the emulator
                        return_code = run(
                            args.romfile,
                            get_gb_input,
                            app_session=app_session,
                            audio_out=audio_out,
                            frame_advance=args.frame_advance,
                            color_mode=args.color_mode,
                            break_after=args.break_after,
                            speed_factor=args.speed_factor,
                            use_cpr_sync=args.cpr_sync,
                            save_directory=save_directory,
                            force_gameboy=args.force_gameboy,
                        )

            # Deal with ctrl+c and ctrl+d exceptions
            except (KeyboardInterrupt, EOFError):
                pass

            # Exit with return code
            else:
                exit(return_code)

            # Restore terminal to its initial state
            finally:
                # Wait for a possible CPR
                time.sleep(0.1)
                # Clear alternate screen
                app_session.input.read_keys()
                app_session.output.erase_screen()
                app_session.output.quit_alternate_screen()
                app_session.output.show_cursor()
                app_session.output.flush()


if __name__ == "__main__":
    main()
