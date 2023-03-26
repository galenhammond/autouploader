import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
import os
import sys
from file_monitor import main as file_monitor_main
from multiprocessing import Process


def main() -> None:
    log = logging.getLogger()

    # if not os.path.exists("./user_files/scheduled"):
    #     try:
    #         os.mkdir("./user_files/scheduled")
    #     except FileExistsError:
    #         log.error(
    #             "Failed to create user_files/scheduled directory. Directory already exists."
    #         )

    try:
        monitor_p: Process = Process(target=file_monitor_main)
        monitor_p.start()
        log.info("File monitor process started.")
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


def get_upload_file_paths(path: str) -> list[str]:
    if not path:
        return []
    return [
        os.path.join(path, file) for file in os.listdir(path) if file.endswith(".mp3")
    ]


if __name__ == "__main__":
    main()
