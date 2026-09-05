from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dataset import load_tasks
from .render import RenderConfig, render_instruction


def main() -> None:
    parser = argparse.ArgumentParser(description="Render benchmark instruction images.")
    parser.add_argument("--tasks", type=Path, default=Path("dataset/tasks.jsonl"))
    parser.add_argument("--out", type=Path, default=Path("rendered"))
    parser.add_argument("--font", default="jetbrains-mono")
    parser.add_argument("--size", type=int, default=14)
    parser.add_argument("--line-gap", type=int, default=1)
    parser.add_argument("--margin", type=int, default=1)
    parser.add_argument("--max-aspect", type=float, default=2.0)
    parser.add_argument("--patch-multiplier", type=float, default=1.2)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    cfg = RenderConfig(
        font_id=args.font,
        font_size_px=args.size,
        line_gap_px=args.line_gap,
        margin_px=args.margin,
        max_aspect_ratio=args.max_aspect,
        patch_token_multiplier=args.patch_multiplier,
    )
    tasks = load_tasks(args.tasks)
    if args.limit is not None:
        tasks = tasks[: args.limit]
    manifest = []
    for task in tasks:
        path = args.out / args.font / f"{args.size}px" / f"{task.task_id}.png"
        result = render_instruction(task.instruction, path, cfg)
        manifest.append({"task_id": task.task_id, **result.__dict__})
        print(f"{task.task_id}: {result.width}x{result.height}, {result.patches} patches")

    out_manifest = args.out / args.font / f"{args.size}px" / "manifest.json"
    out_manifest.parent.mkdir(parents=True, exist_ok=True)
    out_manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_manifest}")


if __name__ == "__main__":
    main()
