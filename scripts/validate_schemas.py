from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


SPARK_TYPES = {
    "string",
    "boolean",
    "byte",
    "short",
    "integer",
    "long",
    "float",
    "double",
    "date",
    "timestamp",
}
SNAKE_CASE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")


def _validate_schema(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        document: Any = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"{path}: cannot parse YAML: {exc}"]

    if not isinstance(document, dict):
        return [f"{path}: root must be a YAML mapping"]

    table_name = document.get("table_name")
    if not isinstance(table_name, str) or not SNAKE_CASE.fullmatch(table_name):
        errors.append(f"{path}: table_name must use snake_case")

    if not isinstance(document.get("description"), str):
        errors.append(f"{path}: description is required")

    columns = document.get("columns")
    if not isinstance(columns, list) or not columns:
        errors.append(f"{path}: columns must be a non-empty list")
        return errors

    column_names: set[str] = set()
    for index, column in enumerate(columns):
        prefix = f"{path}: columns[{index}]"
        if not isinstance(column, dict):
            errors.append(f"{prefix} must be a mapping")
            continue

        name = column.get("name")
        if not isinstance(name, str) or not SNAKE_CASE.fullmatch(name):
            errors.append(f"{prefix}.name must use snake_case")
        elif name in column_names:
            errors.append(f"{prefix}.name is duplicated: {name}")
        else:
            column_names.add(name)

        if column.get("type") not in SPARK_TYPES:
            errors.append(f"{prefix}.type must be one of {sorted(SPARK_TYPES)}")
        if not isinstance(column.get("description"), str):
            errors.append(f"{prefix}.description is required")

    partitions = document.get("partitions", [])
    if not isinstance(partitions, list):
        errors.append(f"{path}: partitions must be a list")
    else:
        for partition in partitions:
            if partition not in column_names:
                errors.append(f"{path}: partition is not a declared column: {partition}")

    return errors


def validate_schemas(schema_root: Path) -> list[str]:
    schema_files = sorted(schema_root.rglob("*.yml")) + sorted(schema_root.rglob("*.yaml"))
    if not schema_files:
        return [f"{schema_root}: no YAML schema files found"]

    errors: list[str] = []
    for schema_file in schema_files:
        errors.extend(_validate_schema(schema_file))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate project YAML schema contracts.")
    parser.add_argument(
        "schema_root",
        nargs="?",
        type=Path,
        default=Path("schemas"),
        help="Schema directory (default: schemas)",
    )
    args = parser.parse_args()

    errors = validate_schemas(args.schema_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"Validated YAML schemas under {args.schema_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
