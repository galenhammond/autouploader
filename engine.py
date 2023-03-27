import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
import os
import config
from argparse import _SubParsersAction, Namespace, ArgumentParser
import sys
import run.run as run
from multiprocessing import Process

RUN_MODES = {
    "run": run,
}


def main() -> None:
    log = logging.getLogger()
    parser: ArgumentParser = ArgumentParser(description="Run a service.")
    parser.add_argument("--version", "-v", action="version", version="%(prog)s 1.0.0")
    subparsers = parser.add_subparsers(dest="run_mode")
    for mode in RUN_MODES.keys():
        subparser = subparsers.add_parser(mode)
        RUN_MODES[mode].build_parser(subparser)

    args: Namespace = parser.parse_args()
    print(args)
    run_mode: str = args.run_mode

    try:
        RUN_MODES[run_mode].run(args)
    except ModuleNotFoundError:
        log.error("Non-existent run mode #{run_mode} specified. Exiting...")
        sys.exit(-1)


if __name__ == "__main__":
    main()
