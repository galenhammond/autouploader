from argparse import ArgumentParser, Namespace
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
        log.error(
            "Invalid service name specified. Use --help for more information. Exiting."
        )
        sys.exit(-1)
    run_service(args.service_name)


def run_service(service_name: str) -> None:
    try:
        service_p: Process = Process(target=RUN_MODES[service_name].run)
        service_p.start()
        log.info(f"Started {service_name} process with PID {service_p.pid}.")
    except OSError:
        log.error(f"Failed to start {service_name} process.")
        sys.exit(-1)

    try:
        service_p.join()
    except KeyboardInterrupt:
        log.info(
            f"Keyboard interrupt detected. Terminating {service_name} with PID {service_p.pid}."
        )
        service_p.terminate()
        service_p.join()
        sys.exit(0)


def build_parser(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--service",
        "-s",
        dest="service_name",
        type=str,
    )
    return
