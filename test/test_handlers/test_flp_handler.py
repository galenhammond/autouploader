import unittest
import sys

sys.path.append("..")


class TestFLPHandler(unittest.TestCase):
    # onCreate() tests
    def test_on_create(self):
        self.assertRaises(AttributeError, run.run, None)
        self.assertLogs("run", "ERROR")
