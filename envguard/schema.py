from typing import Any, Dict, Type


class SchemaError(Exception):
    """Base error for schema definition issues."""

class InvalidSchemaError(SchemaError):
    """Raise when the schema definition is invalid."""

class Schema:
    """
    Base class for environment variable schemas.

    Users subclass this and define env vars using type annotations.
    """

    __fields__: Dict[str, Dict[str, Any]] = {}

    def __init_subclass(cls: Type["Schema"]) -> None:
        super().__init_subclass__()

        fields: Dict[str, Dict[str, Any]] = {}

        annotations = getattr(cls, "__annotations__", {})

        for name, expected_type in annotations.items():
            # Ignore private fields
            if name.startswith("_"):
                continue

            default = getattr(cls, name, None)
            required = not hasattr(cls, name)

            # Validate supported types
            if expected_type not in (str, int, float, bool):
                raise InvalidSchemaError(
                    f"Unsupported type for '{name}': {expected_type}."
                    "Only str, int, float, bool are supported."
                )
            
            fields[name] = {
                "type": expected_type,
                "required": required,
                "default": None if required else default,
            }

        if not fields:
            raise InvalidSchemaError("Schema must define at least one environment variable.")
        
        cls.__fields__ = fields