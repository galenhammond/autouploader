import unittest
import sys
from handlers.flp_handler import FLPEventHandler

sys.path.append("..")

from run import run
from argparse import Namespace


class TestFLPHandler(unittest.TestCase):
    # onCreate() tests
    def test_on_create(self):
        self.assertRaises(AttributeError, run.run, None)
        self.assertLogs("run", "ERROR")
