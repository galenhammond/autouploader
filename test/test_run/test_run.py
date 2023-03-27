import unittest
import sys

sys.path.append("..")

from run import run
from argparse import Namespace


class TestRun(unittest.TestCase):
    def test_logs_error_with_none_args(self):
        self.assertRaises(AttributeError, run.run, None)
        self.assertLogs("run", "ERROR")

    def test_logs_error_with_no_service_name(self):
        args = Namespace()
        self.assertLogs("run", "ERROR")
        self.assertRaises(AttributeError, run.run, args)
