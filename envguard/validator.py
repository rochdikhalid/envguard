from typing import Any, Dict

from .errors import ValidationError
from .schema import Schema
from .loader import EnvLoader

class EnvValidator:
    """Validates env variables against a Schema."""

    def __init__(self, schema: type[Schema]) -> None:
        self.schema = schema
        self.fields = schema.__fields__

    def validate(self) -> Dict[str, Any]:
        loader = EnvLoader(self.schema)
        values, cast_errors = loader.load()

        errors: list[str] = []
        final_config: Dict[str, Any] = {}

        for name, meta in self.fields.items():
            if name in cast_errors:
                errors.append(f"{name} → {cast_errors[name]}")

            if name in values:
                final_config[name] = values[name]
                continue

            if meta["required"]:
                errors.append(f"{name} is missing")
                continue

            final_config[name] = meta["default"]

        if errors:
            raise ValidationError(errors)
        
        return final_config