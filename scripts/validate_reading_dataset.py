#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from vce.dataset import load_tasks

EXPECTED_CATEGORIES = {
    "reading_fact",
    "reading_date",
    "reading_quantity",
    "reading_cause",
    "reading_location",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the synthetic reading-comprehension dataset.")
    parser.add_argument("path", type=Path, nargs="?", default=Path("dataset/reading_200.jsonl"))
    parser.add_argument("--metadata", type=Path, default=Path("dataset/reading_200.metadata.json"))
    parser.add_argument("--expected-count", type=int, default=200)
    parser.add_argument("--min-words", type=int, default=90)
    parser.add_argument("--max-words", type=int, default=180)
    args = parser.parse_args()

    tasks = load_tasks(args.path)
    if len(tasks) != args.expected_count:
        raise SystemExit(f"expected {args.expected_count} tasks, found {len(tasks)}")

    ids = [task.task_id for task in tasks]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate task IDs found")

    passages = [task.instruction.strip() for task in tasks]
    if len(passages) != len(set(passages)):
        raise SystemExit("duplicate passages found")

    category_counts = Counter(task.category for task in tasks)
    if set(category_counts) != EXPECTED_CATEGORIES:
        raise SystemExit(f"unexpected categories: {dict(category_counts)}")

    expected_per_category = args.expected_count // len(EXPECTED_CATEGORIES)
    if any(category_counts[category] != expected_per_category for category in EXPECTED_CATEGORIES):
        raise SystemExit(f"dataset is not balanced across categories: {dict(category_counts)}")

    word_counts: list[int] = []
    for task in tasks:
        if task.scorer != "normalized_scalar":
            raise SystemExit(f"{task.task_id}: expected normalized_scalar scorer, got {task.scorer!r}")
        if not task.payload.strip():
            raise SystemExit(f"{task.task_id}: empty question")
        if not isinstance(task.expected, str) or not task.expected.strip():
            raise SystemExit(f"{task.task_id}: expected answer must be a non-empty string")
        if task.expected.casefold() not in task.instruction.casefold():
            raise SystemExit(f"{task.task_id}: expected answer is not present in passage")
        words = len(task.instruction.split())
        word_counts.append(words)
        if not args.min_words <= words <= args.max_words:
            raise SystemExit(
                f"{task.task_id}: passage has {words} words; expected {args.min_words}..{args.max_words}"
            )

    if args.metadata.exists():
        metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
        if int(metadata.get("count", -1)) != len(tasks):
            raise SystemExit("metadata count does not match dataset")
        if int(metadata.get("seed", -1)) < 0:
            raise SystemExit("metadata seed is missing or invalid")

    print(f"validated {len(tasks)} synthetic reading tasks")
    print("categories:", dict(sorted(category_counts.items())))
    print(
        f"passage words: min={min(word_counts)} mean={sum(word_counts)/len(word_counts):.1f} max={max(word_counts)}"
    )


if __name__ == "__main__":
    main()
