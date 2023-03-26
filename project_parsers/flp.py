import sys

sys.path.append("..")
import os
from logging import getLogger
import pyflp as pf
from .base import ProjectParser
from typing import Optional
import jsonpickle

log = getLogger(__name__)


class FLPProjectParser(ProjectParser):
    @classmethod
    def parse(cls, project_path: str) -> Optional[pf.project.Project]:
        if not os.path.exists(project_path):
            log.error(f"File {project_path} does not exist.")
            return None

        flp: Optional[pf.project.Project] = None

        try:
            flp = pf.parse(project_path)
        except (pf.exceptions.HeaderCorrupted, pf.exceptions.VersionNotDetected) as e:
            log.error(e)

        return flp

    @classmethod
    def serialize(cls, object: object):
        return jsonpickle.encode(
            object,
        )

    @classmethod
    def deserialize(cls, object: object):
        return jsonpickle.decode(object, keys=True)
