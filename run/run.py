from argparse import _SubParsersAction, ArgumentParser, Namespace
from cgi import parse_multipart
import sys
from logging import getLogger
import run.services.scheduler as scheduler
import run.services.file_monitor as file_monitor
from multiprocessing import Process

RUN_MODES = {
    "scheduler": scheduler,
    "file_monitor": file_monitor,
}

log = getLogger(__name__)


def run(args: Namespace) -> None:
    if not args.service_name or args.service_name not in RUN_MODES.keys():
        log.error("Invalid service name specified. Exiting...")
        sys.exit(-1)
    run_service(args.service_name)


def run_service(service_name: str):
    try:
        monitor_p: Process = Process(target=RUN_MODES[service_name].run)
        monitor_p.start()
        log.info(f"Started {service_name} process.")
    except OSError:
        log.error("Failed to start file monitor process.")
        sys.exit(-1)

    try:
        monitor_p.join()
    except KeyboardInterrupt:
        log.info("Keyboard interrupt detected. Shutting down.")
        monitor_p.terminate()
        monitor_p.join()
        sys.exit(0)


def build_parser(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--service",
        "-s",
        dest="service_name",
        type=str,
    )
    return
