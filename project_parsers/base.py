from abc import ABC, abstractmethod


class ProjectParser(ABC):
    """Abstract class for project parsers.
    All project parsers should inherit from this class
    and implement the parse and generate_project_tree methods."""

    @abstractmethod
    def parse(self, project_path):
        pass

    @abstractmethod
    def serialize(self, object: object):
        pass

    @abstractmethod
    def deserialize(self, object: bytes):
        pass
