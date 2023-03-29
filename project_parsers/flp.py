import sys

sys.path.append("..")
import os
from logging import getLogger
from pyflp.exceptions import HeaderCorrupted, VersionNotDetected
from pyflp.project import Project
from pyflp import parse
from .base import ProjectParser
from typing import Optional
from auth.upload_policy import UploadPolicy
import jsonpickle
from config import Config

log = getLogger(__name__)


class FLPProjectParser(ProjectParser):
    @staticmethod
    def parse(project_path: str) -> Optional[Project]:
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
    def is_project_file(path: str) -> bool:
        return path.endswith(".flp")

    @staticmethod
    def serialize(object: object):
        return jsonpickle.encode(
            object,
        )

    @staticmethod
    def deserialize(object: object):
        return jsonpickle.decode(object, keys=True)

    @classmethod
    def prepare_for_export(cls, project_path: str) -> Optional[dict[str, str]]:
        if not cls.is_project_file(project_path):
            return None

        flp_project: Optional[Project] = FLPProjectParser.parse(project_path)
        project_info: dict[str, Optional[str]] = (
            __get_info(flp_project) if flp_project else {}
        )

        upload_metadata: dict[str, str] = __get_upload_metadata_from_info(project_info)
        upload_metadata["project_path"] = project_path
        return upload_metadata


def __get_info(project: Project) -> dict[str, Optional[str]]:
    project_info: dict[str, Optional[str]] = {
        "title": project.title,
        "description": project.comments,
        "genre": project.genre,
        "artists": project.artists,
        "url": project.url,
    }

    return project_info


def __get_upload_metadata_from_info(
    project_info: dict[str, Optional[str]]
) -> dict[str, str]:
    description_and_tags: dict[str, Optional[str]] = __parse_description(
        project_info["description"]
    )
    # image_url = download(
    #     description_and_tags["image_url"],
    #     Config.get_env("USER_ARTWORKS_DIR"),
    # )

    return {
        "upload_title": project_info["title"] or "",
        "upload_tags": description_and_tags["tags"] or "",
        "upload_description": description_and_tags["description"] or "",
        "upload_genre": project_info["genre"] or "",
        "upload_artists": project_info["artists"] or "",
        "upload_cover_art_url": project_info["url"] or "",
    }


def __parse_description(description: Optional[str]) -> dict[str, Optional[str]]:
    # print(description)
    return {}
