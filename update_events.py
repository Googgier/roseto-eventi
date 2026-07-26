#!/usr/bin/env python3
"""Legge, valida e aggiorna esclusivamente data/events.json."""

import argparse
import json
from datetime import date
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
EVENTS_PATH = REPO_DIR / "data" / "events.json"
REQUIRED_FIELDS = {
    "id", "startDate", "endDate", "displayDate", "time", "title", "venue",
    "city", "description", "tags", "sourceUrl", "price", "image", "updatedAt",
}
VALID_PRICES = {"gratis", "a pagamento", "misto"}


def read_events(path=EVENTS_PATH):
    with path.open(encoding="utf-8") as handle:
        events = json.load(handle)
    validate_events(events)
    return events


def validate_events(events):
    if not isinstance(events, list):
        raise ValueError("Il file deve contenere un array JSON")
    ids = set()
    for index, event in enumerate(events):
        missing = REQUIRED_FIELDS - event.keys()
        if missing:
            raise ValueError(f"Evento {index}: campi mancanti: {sorted(missing)}")
        if event["id"] in ids:
            raise ValueError(f"ID duplicato: {event['id']}")
        ids.add(event["id"])
        start = date.fromisoformat(event["startDate"])
        end = date.fromisoformat(event["endDate"])
        date.fromisoformat(event["updatedAt"])
        if end < start:
            raise ValueError(f"Evento {event['id']}: endDate precede startDate")
        if event["price"] not in VALID_PRICES:
            raise ValueError(f"Evento {event['id']}: price non valido")
        if not isinstance(event["tags"], list) or not event["tags"]:
            raise ValueError(f"Evento {event['id']}: tags deve essere un array non vuoto")


def write_events(events, path=EVENTS_PATH):
    validate_events(events)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(events, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        metavar="FILE",
        type=Path,
        help="Sostituisce data/events.json con gli eventi contenuti nel file indicato",
    )
    args = parser.parse_args()
    if args.write:
        with args.write.open(encoding="utf-8") as handle:
            write_events(json.load(handle))
    events = read_events()
    print(f"{len(events)} eventi validi in {EVENTS_PATH}")


if __name__ == "__main__":
    main()
