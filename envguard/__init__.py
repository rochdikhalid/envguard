from .schema import Schema
from .validator import EnvValidator

__all__ = ["schema", "load", "export_example"]

def load(schema: type[Schema]):
    """Validate env variables and return typed config."""
    validator = EnvValidator(schema)
    return validator.validate()