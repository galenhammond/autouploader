from abc import ABCMeta, abstractclassmethod, abstractmethod


class ProjectParser(ABCMeta):
    """Abstract class for project parsers.
    All project parsers should inherit from this class
    and implement the parse and serialize/deserialize methods."""

    @abstractmethod
    def parse(self, project_path):
        pass

    @abstractclassmethod
    def serialize(self, object: object):
        pass

    @abstractclassmethod
    def deserialize(self, object: object):
        pass
