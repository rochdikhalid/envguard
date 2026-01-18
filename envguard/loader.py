import os
from typing import Any, Dict, Tuple

from .schema import Schema


class EnvLoader:
    """
    Loads env vars and casts them according to a Schema
    """

    def __init__(self, schema: type[Schema]) -> None:
        self.schema = schema
        self.fields = schema.__fields__

    def load(self) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        Load and cast environment variables.
        Returns:
            values: successfully cast values
            errors: casting errors (name -> error message)
        """
        values: Dict[str, Any] = {}
        errors: Dict[str, str] = {}

        for name, meta in self.fields.items():
            raw_value = os.environ.get(name)

            if raw_value is None:
                continue

            try:
                values[name] = self.__cast(raw_value, meta["type"])
            except ValueError as exc:
                errors[name]: str(exc)

        return values, errors
    
    def _cast(self, value: str, expected_type: type) -> Any:
        """Cast string env value to expected type."""
        if expected_type is str:
            return value
        
        if expected_type is int:
            return int(value)
        
        if expected_type is float:
            return float(value)
        
        if expected_type is bool:
            return self._parse_bool(value)
        
        raise ValueError(f"Unsupported type: {expected_type}")
    
    def _parse_bool(self, value: str) -> bool:
        normalized = value.strip().lower()

        if normalized in ("true", "1", "yes", "on"):
            return True
        if normalized in ("false", "0", "no", "off"):
            return False
        
        raise ValueError(
            f"Invalid boolean value '{value}'."
            "Expected one of: true/false, 1/0, yes/no, on/off."
        )