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
    def serialize(cls, flp: pf.project.Project) -> str:
        return jsonpickle.encode(flp)

    @classmethod
    def deserialize(cls, data: str) -> Optional[pf.project.Project]:
        return jsonpickle.decode(data, classes=(pf.project.Project))