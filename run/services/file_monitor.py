import sys

sys.path.append("..")
import time
from logging import getLogger
from config import Config
from watchdog.observers import Observer
from handlers.flp_handler import FLPEventHandler

log = getLogger("__main__." + __name__)


def run():
    path = Config.get_env("MIXDOWN_DIR")
    if not path:
        return
    event_handler = FLPEventHandler()
    project_file_dir_observer = Observer()
    project_file_dir_observer.schedule(event_handler, path, recursive=True)
    project_file_dir_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        project_file_dir_observer.stop()
    project_file_dir_observer.join()


if __name__ == "__main__":
    run()
