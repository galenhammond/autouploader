import unittest

from pkg_resources import cleanup_resources
from project_parsers.project_tree.fragment import Fragment
from project_parsers.project_tree.project_tree import ProjectTree

SERIALIZED_TREE_STRING = "A:AB:BE:E_F:FK:K___C:C_D:DG:G_H:H_I:I_J:J___"


class TestProjectTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Fragment("A", "A")
        root.children = [
            Fragment("B", "B"),
            Fragment("C", "C"),
            Fragment("D", "D"),
        ]
        root.children[0].children = [Fragment("E", "E"), Fragment("F", "F")]
        root.children[2].children = [
            Fragment("G", "G"),
            Fragment("H", "H"),
            Fragment("I", "I"),
            Fragment("J", "J"),
        ]
        root.children[0].children[1].children = [Fragment("K", "K")]
        cls.tree = ProjectTree(root)

    def test_project_tree_serialize_contains_all_nodes(self):
        serialized_tree = self.tree.serialize()
        self.assertEqual(
            serialized_tree,
            SERIALIZED_TREE_STRING,
        )

    def test_deserialize_contains_all_nodes(self):
        root = ProjectTree.deserialize(SERIALIZED_TREE_STRING)
        tree = ProjectTree(root) if root else None
        if not tree:
            self.fail("tree should not be None")
        self.assertTrue(tree.equals(self.tree), "trees should be equal")
