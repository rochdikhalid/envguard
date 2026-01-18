import argpase 
import sys
from typing import Type

from .schema import Schema
from .validator import EnvValidator
from .exporter import export_example

def main():
    parser = argparse.ArgumentParser(
        description="envguard — fail-fast, human-friendly environment configuration."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # -------- check command --------
    parser_check = subparsers.add_parser(
        "check", help="Validate environment variables against a schema"
    )
    parser_check.add_argument(
        "--schema",
        type=str,
        required=True,
        help="Python path to the schema class (module:ClassName), e.g., config:Config"
    )

    # -------- export command --------
    parser_export = subparsers.add_parser(
        "export", help="Generate .env.example from schema"
    )
    parser_export.add_argument(
        "--schema",
        type=str,
        required=True,
        help="Python path to the schema class (module:ClassName), e.g., config:Config"
    )
    parser_export.add_argument(
        "--output",
        type=str,
        default=".env.example",
        help="Output file (default: .env.example)"
    )

    args = parser.parse_args()

    # Dynamically import schema
    module_path, class_name = args.schema.split(":")
    module = __import__(module_path, fromlist=[class_name])
    schema_class: Type[Schema] = getattr(module, class_name)

    if args.command == "check":
        try:
            validator = EnvValidator(schema_class)
            config = validator.validate()
            print("✅ All environment variables are valid!")
        except Exception as exc:
            print(exc)
            sys.exit(1)

    elif args.command == "export":
        export_example(schema_class, file=args.output)
        print(f"✅ .env.example generated at {args.output}")
