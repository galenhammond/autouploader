import unittest

import pyflp

from project_parsers.flp import FLPProjectParser
from typing import Optional
import pyflp as pf
import config


class TestProjectTree(unittest.TestCase):
    def test_parses_flp_with_no_error(self):
        project: Optional[pf.project.Project] = FLPProjectParser.parse(
            config.TEST_FLP_PATH
        )
        self.assertIsNotNone(project, "project should not be None")

    def test_serialize_converts_project_to_json(self):
        project: Optional[pf.project.Project] = FLPProjectParser.parse(
            config.TEST_FLP_PATH
        )
        if project:
            json = FLPProjectParser.serialize(project)
            self.assertIsInstance(json, str, "json should be a string")

    def test_deserialize_converts_string_to_project(self):
        project: Optional[pf.project.Project] = FLPProjectParser.parse(
            config.TEST_FLP_PATH
        )
        if project:
            json = FLPProjectParser.serialize(project)
            decoded_project = FLPProjectParser.deserialize(json)
            self.assertIsInstance(
                decoded_project,
                pf.project.Project,
                "decoded_project should be a pf.project.Project",
            )
