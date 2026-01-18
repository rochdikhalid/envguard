import unittest
from envguard.schema import Schema, InvalidSchemaError

class TestSchema(unittest.TestCase):

    def test_required_and_optional_fields(self):
        class Config(Schema):
            PORT: int
            DEBUG: bool = False

        fields = Config.__fields__
        self.assertEqual(fields["PORT"]["required"], True)
        self.assertEqual(fields["DEBUG"]["required"], False)
        self.assertEqual(fields["DEBUG"]["default"], False)

    def test_invalid_type(self):
        with self.assertRaises(InvalidSchemaError):
            class BadConfig(Schema):
                SECRET: dict
