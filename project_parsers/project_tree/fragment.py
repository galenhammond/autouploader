from __future__ import annotations
from . import utils


class Fragment:
    def __init__(self, key: str, value: str, children: list[Fragment] = []) -> None:
        self.key = key
        self.value = value
        self.children = children
        return

    def serialize(self) -> list[str]:
        vals: list[str] = []
        vals.append(self.key + utils.KEY_VALUE_SEPARATOR + self.value)
        for child in self.children:
            vals.extend(child.serialize())
        # Store a level marker at the end of children
        vals.append(utils.TREE_EOL_MARKER)
        return vals

    def equals(self, other: Fragment) -> bool:
        if self.key != other.key or self.value != other.value:
            return False
        if len(self.children) != len(other.children):
            return False
        for i in range(len(self.children)):
            if not self.children[i].equals(other.children[i]):
                return False
        return True
