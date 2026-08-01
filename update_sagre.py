#!/usr/bin/env python3
"""Legge, valida e aggiorna esclusivamente data/sagre.json."""

import argparse
import json
from datetime import date
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
SAGRE_PATH = REPO_DIR / "data" / "sagre.json"
SCHEMA_PATH = REPO_DIR / "data" / "sagre.schema.json"
REQUIRED_FIELDS = {
    "id", "startDate", "endDate", "displayDate", "title", "venue",
    "province", "sourceLabel", "updatedAt",
}
PROVINCES = {"AQ", "CH", "PE", "TE"}
SOURCE_LABEL = "Sagre in Abruzzo — Agosto 2026"


def validate_sagre(sagre):
    if not isinstance(sagre, list):
        raise ValueError("Il file deve contenere un array JSON")
    ids = set()
    for index, sagra in enumerate(sagre):
        if set(sagra) != REQUIRED_FIELDS:
            raise ValueError(f"Sagra {index}: campi non conformi allo schema")
        if sagra["id"] in ids:
            raise ValueError(f"ID duplicato: {sagra['id']}")
        ids.add(sagra["id"])
        start = date.fromisoformat(sagra["startDate"])
        end = date.fromisoformat(sagra["endDate"])
        date.fromisoformat(sagra["updatedAt"])
        if start.year != 2026 or start.month != 8 or end.year != 2026 or end.month != 8:
            raise ValueError(f"Sagra {sagra['id']}: data fuori da agosto 2026")
        if end < start:
            raise ValueError(f"Sagra {sagra['id']}: endDate precede startDate")
        if sagra["province"] not in PROVINCES:
            raise ValueError(f"Sagra {sagra['id']}: provincia non valida")
        if sagra["sourceLabel"] != SOURCE_LABEL:
            raise ValueError(f"Sagra {sagra['id']}: fonte non valida")
        for field in ("id", "displayDate", "title", "venue"):
            if not isinstance(sagra[field], str) or not sagra[field].strip():
                raise ValueError(f"Sagra {sagra['id']}: {field} vuoto")


def read_sagre(path=SAGRE_PATH):
    with path.open(encoding="utf-8") as handle:
        sagre = json.load(handle)
    validate_sagre(sagre)
    return sagre


def write_sagre(sagre, path=SAGRE_PATH):
    validate_sagre(sagre)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(sagre, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", metavar="FILE", type=Path,
                        help="Sostituisce data/sagre.json con il file indicato")
    args = parser.parse_args()
    if args.write:
        with args.write.open(encoding="utf-8") as handle:
            write_sagre(json.load(handle))
    sagre = read_sagre()
    print(f"{len(sagre)} sagre valide in {SAGRE_PATH}")


if __name__ == "__main__":
    main()
