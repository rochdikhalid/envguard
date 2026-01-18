import argparse
import sys
from typing import Dict, Type

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

    # -------- diff command --------
    parser_diff = subparsers.add_parser(
        "diff", help="Compare two .env files"
    )
    parser_diff.add_argument("file_a", type=str, help="Path to first .env file")
    parser_diff.add_argument("file_b", type=str, help="Path to second .env file")    

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

    elif args.command == "diff":
        def load_file(file_path: str) -> Dict[str, str]:
            env_dict = {}
            with open(file_path) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    env_dict[k.strip()] = v.strip()
            return env_dict

        env_a = load_file(args.file_a)
        env_b = load_file(args.file_b)

        from .diff import diff_envs

        result = diff_envs(env_a, env_b)
        print(result)
