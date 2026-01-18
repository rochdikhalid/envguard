import os
import unittest
from envguard.schema import Schema
from envguard.loader import EnvLoader

class TestLoader(unittest.TestCase):

    def setUp(self):
        os.environ.clear()

    def test_casting_success(self):
        os.environ["PORT"] = "8080"
        os.environ["DEBUG"] = "true"

        class Config(Schema):
            PORT: int
            DEBUG: bool

        loader = EnvLoader(Config)
        values, errors = loader.load()
        self.assertEqual(values["PORT"], 8080)
        self.assertEqual(values["DEBUG"], True)
        self.assertEqual(errors, {})

    def test_casting_error(self):
        os.environ["PORT"] = "abc"

        class Config(Schema):
            PORT: int

        loader = EnvLoader(Config)
        values, errors = loader.load()
        self.assertIn("PORT", errors)
