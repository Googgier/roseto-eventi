#!/usr/bin/env python3
"""Valida entrambi i dataset contro gli schemi, mantenendoli indipendenti."""

import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent


def validate(name):
    with (ROOT / "data" / f"{name}.json").open(encoding="utf-8") as handle:
        data = json.load(handle)
    with (ROOT / "data" / f"{name}.schema.json").open(encoding="utf-8") as handle:
        schema = json.load(handle)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(data)
    print(f"{name}: schema valido, {len(data)} record")


if __name__ == "__main__":
    validate("events")
    validate("sagre")
