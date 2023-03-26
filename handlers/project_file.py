import sys

sys.path.append("..")
from logging import getLogger
from typing import Optional
from watchdog.events import FileSystemEventHandler, FileSystemEvent, FileMovedEvent
from project_parsers.flp import FLPProjectParser
from pyflp.project import Project
import pprint as pp


class ProjectFileEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.log = getLogger(__name__)

    def on_created(self, event: FileSystemEvent):
        super().on_created(event)

        what = "directory" if event.is_directory else "file"
        self.log.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event: FileSystemEvent):
        super().on_deleted(event)

        what = "directory" if event.is_directory else "file"
        self.log.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event: FileSystemEvent):
        super().on_modified(event)

        what = "directory" if event.is_directory else "file"
        self.log.info("Modified %s: %s", what, event.src_path)

        if not event.is_directory and event.src_path.endswith(".flp"):
            flp_project: Optional[Project] = FLPProjectParser.parse(event.src_path)
            if flp_project:
                serialized_project = FLPProjectParser.serialize(flp_project)
                pp.pprint(serialized_project)

    def on_moved(self, event: FileMovedEvent):
        super().on_moved(event)

        what = "directory" if event.is_directory else "file"
        self.log.info("Moved %s: from %s to %s", what, event.src_path, event.dest_path)

    def on_closed(self, event: FileSystemEvent):
        super().on_closed(event)
