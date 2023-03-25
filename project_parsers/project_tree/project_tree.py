from __future__ import annotations
from email import iterators
from .fragment import Fragment
from . import utils
from typing import Optional


class ProjectTree:
    def __init__(self, root: Fragment, serialized_string: Optional[str] = None) -> None:
        if not root and not serialized_string:
            # TODO: Figure out how to handle this case
            raise Exception("Either root or serialized_string must be provided")
        self.root = root
        self.serialized_string = serialized_string
        return

    def equals(self, other: ProjectTree) -> bool:
        return self.root.equals(other.root)

    def serialize(self) -> str:
        vals: list[str] = self.root.serialize()
        return "".join(vals)

    @staticmethod
    def deserialize(data: str) -> Optional[Fragment]:
        def isplit(source, sep):
            sepsize = len(sep)
            start = 0
            while True:
                idx = source.find(sep, start)
                if idx == -1:
                    yield source[start:]
                    return
                yield source[start:idx]
                start = idx + sepsize

        def dfs(vals):
            key = next(vals)
            if key == utils.TREE_EOL_MARKER:
                return None
            colon = next(vals, None)
            value = next(vals)
            root = Fragment(key=key, value=value)
            child = dfs(vals)
            while child:
                root.children.append(child)
                child = dfs(vals)
            return root

        if not data:
            return None

        return dfs(iter(isplit(data, " ")))
