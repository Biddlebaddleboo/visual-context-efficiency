#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import random

DEFAULT_SEED = 20260905
DEFAULT_COUNT = 200

NAMES = ["Mira","Jonas","Leila","Owen","Priya","Mateo","Nora","Caleb","Aisha","Victor","Elena","Darius","Sofia","Ravi","Tessa","Hugo","Naomi","Felix","Iris","Malik"]
CITIES = ["Harbourton","Redvale","Northbridge","Lakehurst","Cedarfield","Westmere","Stonehaven","Ashford","Pinecrest","Rivermouth","Glenhaven","Maplewick"]
COLORS = ["amber","cobalt","indigo","scarlet","teal","violet","silver","ochre","crimson","jade","bronze","ivory"]
ITEMS = ["ledger","sensor","crate","binder","package","sample","module","folder","kit","parcel","notebook","case"]
PLACES = ["east annex","west depot","upper archive","river lab","south workshop","central office","north warehouse","field station","training room","dispatch bay"]
REASONS = [
    "a power inspection was scheduled",
    "the delivery truck arrived late",
    "the temperature sensor failed",
    "a safety drill occupied the main hall",
    "the network maintenance window was extended",
    "the replacement key had not arrived",
    "heavy rain delayed the outdoor work",
    "the inventory count took longer than expected",
    "a supplier changed the pickup time",
    "the calibration check had to be repeated",
]
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
TYPES = ["fact","date","quantity","cause","location"]


def filler_sentence(rng: random.Random) -> str:
    n1, n2 = rng.sample(NAMES, 2)
    city = rng.choice(CITIES)
    place = rng.choice(PLACES)
    item = rng.choice(ITEMS)
    return rng.choice([
        f"{n1} reviewed the {item} in the {place} while {n2} updated a separate checklist.",
        f"The team in {city} closed the morning briefing before lunch and reopened the {place} afterward.",
        f"{n1} noted that the {item} was routine and did not require a special approval.",
        f"A separate shipment for {city} was logged by {n1}, but it was unrelated to the main assignment.",
        f"{n1} and {n2} compared their notes in the {place} before moving on to ordinary maintenance.",
    ])


def build_rows(count: int = DEFAULT_COUNT, seed: int = DEFAULT_SEED) -> list[dict]:
    rng = random.Random(seed)
    rows: list[dict] = []
    for i in range(count):
        kind = TYPES[i % len(TYPES)]
        subject = rng.choice(NAMES)
        sentences = [filler_sentence(rng) for _ in range(5)]

        if kind == "fact":
            answer = rng.choice(COLORS)
            target = (
                f"For the current review, {subject} marked the {rng.choice(ITEMS)} with the code word {answer}, "
                "which was the only code authorized for that record."
            )
            question = f"What code word did {subject} use for the current review?"
        elif kind == "date":
            answer = f"{rng.choice(MONTHS)} {rng.randint(2, 27)}"
            target = (
                f"The final inspection assigned to {subject} was moved to {answer} after the earlier tentative "
                "date was cancelled."
            )
            question = f"On what date was {subject}'s final inspection scheduled?"
        elif kind == "quantity":
            answer = str(rng.randint(12, 96))
            item = rng.choice(ITEMS)
            target = (
                f"When the count was finalized, {subject} recorded exactly {answer} {item}s in the active batch; "
                "older stock was tracked separately."
            )
            question = f"How many {item}s were in the active batch recorded by {subject}?"
        elif kind == "cause":
            answer = rng.choice(REASONS)
            target = (
                f"{subject} postponed the afternoon handoff because {answer}; no other issue was listed as the "
                "cause of the delay."
            )
            question = f"Why did {subject} postpone the afternoon handoff?"
        else:
            answer = rng.choice(PLACES)
            target = (
                f"The signed copy assigned to {subject} was stored in the {answer}, not in either of the temporary "
                "staging areas mentioned in older notes."
            )
            question = f"Where was the signed copy assigned to {subject} stored?"

        sentences.insert(rng.randint(1, len(sentences) - 1), target)
        sentences.append(filler_sentence(rng))
        sentences.append(filler_sentence(rng))

        rows.append({
            "task_id": f"reading_{i + 1:03d}",
            "category": f"reading_{kind}",
            "instruction": " ".join(sentences),
            "payload": question,
            "expected": answer,
            "scorer": "normalized_scalar",
            "tags": ["reading_comprehension", "synthetic", kind, "non_coding"],
            "version": 1,
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the deterministic 200-passage reading-comprehension benchmark.")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output", type=Path, default=Path("dataset/reading_200.jsonl"))
    args = parser.parse_args()
    if args.count < 1:
        raise SystemExit("--count must be positive")

    rows = build_rows(args.count, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    words = [len(row["instruction"].split()) for row in rows]
    print(f"wrote {len(rows)} tasks to {args.output}")
    print(f"passage words: min={min(words)} mean={sum(words)/len(words):.1f} max={max(words)}")
    print(f"seed={args.seed}")


if __name__ == "__main__":
    main()
