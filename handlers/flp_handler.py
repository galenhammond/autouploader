import sys

sys.path.append("..")
from logging import getLogger
from typing import Optional
from watchdog.events import FileSystemEventHandler, FileSystemEvent, FileMovedEvent
from project_parsers.flp import FLPProjectParser
from pyflp.project import Project
from project_parsers._utils import try_and_get_project as try_and_get_project


class FLPEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.log = getLogger(__name__)

    def on_created(self, event: FileSystemEvent):
        super().on_created(event)

        what = "directory" if event.is_directory else "file"
        self.log.info("Created %s: %s", what, event.src_path)
        project = try_and_get_project(event.src_path, FLPProjectParser)
        if not project:
            self.log.error(
                "try_and_get_project could not get project from file: %s, skipping additional processing.",
                event.src_path,
            )
            return

        # TODO: handle whether to queue/backup or not

    def on_deleted(self, event: FileSystemEvent):
        super().on_deleted(event)

        what = "directory" if event.is_directory else "file"
        self.log.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event: FileSystemEvent):
        super().on_modified(event)

        what = "directory" if event.is_directory else "file"
        self.log.info("Modified %s: %s", what, event.src_path)
        project: object = try_and_get_project(event.src_path)
        if not project:
            self.log.error(
                "try_and_get_project could not get project from file: %s, skipping additional processing.",
                event.src_path,
            )
            return

        # TODO: handle whether to queue/backup or not

    def on_moved(self, event: FileMovedEvent):
        super().on_moved(event)

        what = "directory" if event.is_directory else "file"
        self.log.info("Moved %s: from %s to %s", what, event.src_path, event.dest_path)

    def on_closed(self, event: FileSystemEvent):
        super().on_closed(event)
