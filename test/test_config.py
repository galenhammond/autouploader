import unittest
import sys

sys.path.append("..")

from config import Config


class TestConfig(unittest.TestCase):
    def test_get_env_returns_correct_value(self):
        value = Config.get_env("PROGRAM_NAME")
        self.assertEqual(value, "emu")

    def test_get_env_returns_default_on_invalid_key(self):
        value = Config.get_env("INVALID_KEY")
        self.assertFalse(value, "value should be False")
