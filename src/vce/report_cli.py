from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize a benchmark results.jsonl file.")
    parser.add_argument("results", type=Path)
    args = parser.parse_args()

    rows = [json.loads(line) for line in args.results.read_text(encoding="utf-8").splitlines() if line.strip()]
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        if row.get("dry_run"):
            continue
        render = row.get("render") or {}
        cfg = render.get("config") or {}
        key = (
            row.get("condition"),
            cfg.get("font_id", "text"),
            cfg.get("font_size_px", "-"),
            cfg.get("line_gap_px", "-"),
        )
        groups[key].append(row)

    print("condition\tfont\tsize\tgap\tvalid\tpass\taccuracy\tmean_patches")
    for key, items in sorted(groups.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
        valid = [r for r in items if not r.get("infrastructure_failure") and r.get("score")]
        passed = sum(1 for r in valid if r["score"].get("passed"))
        accuracy = passed / len(valid) if valid else 0.0
        patches = [r["render"]["patches"] for r in valid if r.get("render")]
        mean_patches = sum(patches) / len(patches) if patches else 0.0
        print("\t".join(map(str, [*key, len(valid), passed, f"{accuracy:.4f}", f"{mean_patches:.2f}"])))


if __name__ == "__main__":
    main()
