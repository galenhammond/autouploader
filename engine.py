import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
import os
from config import Config
from argparse import Namespace, ArgumentParser
import sys
import run.run as run

log = logging.getLogger()
RUN_MODES = {
    "run": run,
}


def main() -> None:
    build_directories()
    parser: ArgumentParser = build_parsers()
    args: Namespace = parser.parse_args()
    run_mode: str = args.run_mode

    if not args or not run_mode or run_mode not in RUN_MODES.keys():
        log.error(
            "Invalid run mode specified. Use --help for more information. Exiting."
        )
        sys.exit(-1)

    try:
        RUN_MODES[run_mode].run(args)
    except (ModuleNotFoundError, KeyError) as e:
        log.error(
            f"Non-existent run mode {run_mode} specified. Use --help for more information. Exiting."
        )
        sys.exit(-1)


def build_parsers() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="Run a service.")
    parser.add_argument("--version", "-v", action="version", version="%(prog)s 1.0.0")

    subparsers = parser.add_subparsers(dest="run_mode")
    for mode in RUN_MODES.keys():
        subparser = subparsers.add_parser(mode)
        RUN_MODES[mode].build_parser(subparser)
    return parser


def build_directories() -> None:
    user_files_dir: str = Config.get_env("USER_FILES_DIR")
    if not os.path.exists(user_files_dir):
        try:
            assert dir_builder(user_files_dir)
        except (FileExistsError, FileNotFoundError, AssertionError) as e:
            log.error(
                f"Failed to create user file directory in {user_files_dir}. Error: {e} Exiting."
            )
            sys.exit(-1)

    if not os.path.exists(Config.get_env("MIXDOWN_DIR")):
        log.error(
            "Failed to create user_files/scheduled directory. Directory already exists."
        )
        sys.exit(-1)
    return None


def dir_builder(path: str) -> bool:
    if not path or os.path.exists(path):
        return False

    path = os.path.expanduser(path)
    path_arr = path.split("/")
    curr_path = ""
    while len(path_arr):
        curr_dir = path_arr.pop(0)
        new_path = f"{curr_path}/{curr_dir}"
        if not os.path.exists(new_path):
            try:
                os.mkdir(new_path)
            except (FileExistsError, FileNotFoundError) as e:
                log.error(f"Failed to build directory {new_path}. Error: {e} Exiting.")
                sys.exit(-1)
        curr_path = new_path
        os.chdir(curr_path)
    os.chdir(Config.get_env("ROOT_FOLDER_PATH"))
    return True


if __name__ == "__main__":
    main()
