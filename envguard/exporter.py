from typing import Type
from .schema import Schema

def export_example(schema: Type[Schema], file: str = ".env.example") -> None:
    """
    Generate a .env.example file from a schema.

    Rules:
    - Required: empty value.
    - Optional: default value.
    - Boolean: lowercase
    """
    lines = []

    for name, meta in schema.__fields__.items():
        value = meta["default"]
        required = meta["required"]

        if required:
            lines.append(f"{name}=")
        else:
            if isinstance(value, bool):
                value_str: str(value).lower()
            else:
                value_str: str(value)
            lines.append(f"{name}={value_str}")

    content = "\n".join(lines) + "\n"

    with open(file, "w") as f:
        f.write(content)