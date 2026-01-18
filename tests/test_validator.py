import os
import unittest
from envguard.schema import Schema
from envguard.validator import EnvValidator
from envguard.errors import ValidationError

class TestValidator(unittest.TestCase):

    def setUp(self):
        os.environ.clear()

    def test_missing_required(self):
        class Config(Schema):
            PORT: int
            DEBUG: bool = False

        validator = EnvValidator(Config)
        with self.assertRaises(ValidationError) as cm:
            validator.validate()

        self.assertIn("PORT is missing", str(cm.exception))

    def test_valid_env(self):
        os.environ["PORT"] = "8000"
        class Config(Schema):
            PORT: int
            DEBUG: bool = False

        validator = EnvValidator(Config)
        config = validator.validate()
        self.assertEqual(config["PORT"], 8000)
        self.assertEqual(config["DEBUG"], False)
