#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import subprocess
import sys

from vce.dataset import load_tasks
from vce.render import RenderConfig, render_instruction


PROMPT_TEMPLATE = (
    "Read the passage in the attached image and answer the question below. "
    "Return only the answer, with no explanation.\n\nQuestion:\n{payload}"
)


def render_passages(tasks_path: Path, font: str, size: int, output_root: Path) -> Path:
    tasks = load_tasks(tasks_path)
    out_dir = output_root / font / f"{size}px"
    manifest_path = out_dir / "manifest.jsonl"
    cfg = RenderConfig(
        font_id=font,
        font_size_px=size,
        line_gap_px=1,
        margin_px=1,
        max_aspect_ratio=None,
        patch_token_multiplier=1.2,
    )

    records: list[dict] = []
    for task in tasks:
        image_path = out_dir / f"{task.task_id}.png"
        result = render_instruction(task.instruction, image_path, cfg)
        records.append({
            "task_id": task.task_id,
            "category": task.category,
            "instruction": task.instruction,
            "font_id": font,
            "font_size_px": size,
            "margin_px": 1,
            "line_gap_px": 1,
            "width": result.width,
            "height": result.height,
            "patch_columns": result.patch_columns,
            "patch_rows": result.patch_rows,
            "patches": result.patches,
            "estimated_image_tokens": result.estimated_image_tokens,
            "line_height_px": result.line_height_px,
            "line_count": result.line_count,
            "font_sha256": result.font_sha256,
            "image_sha256": result.image_sha256,
            "path": result.path,
            "render_config": asdict(cfg),
        })

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    patches = [r["patches"] for r in records]
    tokens = [r["estimated_image_tokens"] for r in records]
    print(f"rendered {len(records)} passages: {font} {size}px")
    print(f"mean patches={sum(patches)/len(patches):.2f}; mean estimated image tokens={sum(tokens)/len(tokens):.2f}")
    print(f"manifest: {manifest_path}")
    return manifest_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render and run the 200-passage visual reading-comprehension benchmark."
    )
    parser.add_argument("--tasks", type=Path, default=Path("dataset/reading_200.jsonl"))
    parser.add_argument("--font", default="fira-sans")
    parser.add_argument("--size", type=int, default=8)
    parser.add_argument("--rendered-root", type=Path, default=Path("rendered/reading-200"))
    parser.add_argument("--runs-root", type=Path, default=Path("runs/reading-200"))
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", type=Path)
    args = parser.parse_args()

    if args.size <= 0:
        raise SystemExit("--size must be positive")
    if args.concurrency < 1:
        raise SystemExit("--concurrency must be at least 1")
    if not args.tasks.exists():
        raise SystemExit(
            f"reading dataset not found: {args.tasks}. Generate it with: "
            "python3 scripts/generate_reading_dataset.py"
        )

    tasks = load_tasks(args.tasks)
    if len(tasks) != 200:
        raise SystemExit(f"expected exactly 200 reading tasks, found {len(tasks)}")

    manifest = render_passages(args.tasks, args.font, args.size, args.rendered_root)

    command = [
        sys.executable,
        "scripts/run_timestamped_rendered_corpus.py",
        "--runs-root",
        str(args.runs_root),
        "--manifest",
        str(manifest),
        "--tasks",
        str(args.tasks),
        "--prompt-template",
        PROMPT_TEMPLATE,
        "--concurrency",
        str(args.concurrency),
    ]
    if args.dry_run:
        command.append("--dry-run")
    if args.resume:
        command.extend(["--resume", str(args.resume)])

    print("+", " ".join(command), flush=True)
    raise SystemExit(subprocess.run(command).returncode)


if __name__ == "__main__":
    main()
