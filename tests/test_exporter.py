import os
import unittest
from tempfile import NamedTemporaryFile
from envguard.schema import Schema
from envguard.exporter import export_example

class TestExporter(unittest.TestCase):

    def test_export_example_file(self):
        class Config(Schema):
            PORT: int
            DEBUG: bool = False

        with NamedTemporaryFile("r+") as tmp:
            export_example(Config, file=tmp.name)
            tmp.seek(0)
            content = tmp.read()

        self.assertIn("PORT=", content)
        self.assertIn("DEBUG=false", content)
