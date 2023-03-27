import sys

sys.path.append("..")
import time
from logging import getLogger
import config  # This is the config file that I have in the same folder as main.py
from watchdog.observers import Observer
from handlers.project_file import ProjectFileEventHandler

log = getLogger("__main__." + __name__)

def run():
    path = config.RENDERED_MIXES_FOLDER_PATH if config else "."
    event_handler = ProjectFileEventHandler()
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
