import sys

sys.path.append("..")
import os
from logging import getLogger
from pyflp.exceptions import HeaderCorrupted, VersionNotDetected
from pyflp.project import Project
from pyflp import parse
from .base import ProjectParser
from typing import Optional
from ._utils import download
import jsonpickle
from config import Config

log = getLogger(__name__)


class FLPProjectParser(ProjectParser):
    @classmethod
    def parse(cls, project_path: str) -> Optional[Project]:
        if not os.path.exists(project_path):
            log.error(f"File {project_path} does not exist.")
            return None

        flp: Optional[Project] = None
        try:
            flp = parse(project_path)
        except (HeaderCorrupted, VersionNotDetected) as e:
            log.error(f"Error occured while parsing {project_path}. Error: {e}")
        return flp

    @staticmethod
    def get_tags(project: Project) -> dict[str, Optional[str]]:
        project_tags: dict[str, Optional[str]] = {
            "title": project.title,
            "comments": project.comments,
            "genre": project.genre,
            "artists": project.artists,
            "url": project.url,
        }
        return project_tags

    @staticmethod
    def is_flp_project_file(path: str) -> bool:
        return path.endswith(".flp")

    @staticmethod
    def get_upload_metadata_from_tags(tags: dict[str, Optional[str]]) -> dict[str, str]:
        # TODO
        description_meta: dict[str, Optional[str]] = _parse_description(tags)
        image_url = download(
            description_meta["image_url"],
            Config.get_env("USER_ARTWORKS_DIR"),
        )

        return {
            "title": tags["title"] or "",
            "description": tags["comments"] or "",
            "genre": tags["genre"] or "",
            "artists": tags["artists"] or "",
            "url": tags["url"] or "",
        }

    @classmethod
    def serialize(cls, object: object):
        return jsonpickle.encode(
            object,
        )

    @classmethod
    def deserialize(cls, object: object):
        return jsonpickle.decode(object, keys=True)


def _parse_description(tags: dict[str, Optional[str]]) -> dict[str, Optional[str]]:
    # TODO
    return {}
