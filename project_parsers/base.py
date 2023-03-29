from abc import ABCMeta, abstractmethod, abstractstaticmethod
from typing import Optional


class ProjectParser(ABCMeta):
    """Abstract class for project parsers.
    All project parsers should inherit from this class
    and implement the parse and serialize/deserialize methods."""

    @abstractstaticmethod
    def parse(project_path: object) -> Optional[object]:
        pass

    @abstractmethod
    def is_project_file(path: object) -> bool:
        pass

    @abstractstaticmethod
    def serialize(object: object) -> object:
        pass

    @abstractstaticmethod
    def deserialize(object: object) -> object:
        pass
