#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from vce.dataset import load_tasks
from vce.fonts import installed_fonts
from vce.render import RenderConfig, render_instruction

DEFAULT_FONTS = [
    "fira-sans",
    "atkinson-hyperlegible",
    "ibm-plex-sans",
    "source-sans-3",
    "inter",
    "noto-sans",
    "jetbrains-mono",
]
CONTROL_FONT = "jetbrains-mono"


def parse_fonts(value: str) -> list[str]:
    fonts = [part.strip() for part in value.split(",") if part.strip()]
    if not fonts:
        raise argparse.ArgumentTypeError("at least one font ID is required")
    return fonts


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render the 200 synthetic reading passages across six candidate fonts plus a control."
    )
    parser.add_argument("--tasks", type=Path, default=Path("dataset/reading_200.jsonl"))
    parser.add_argument("--fonts", type=parse_fonts, default=DEFAULT_FONTS)
    parser.add_argument("--size", type=int, default=8)
    parser.add_argument("--margin", type=int, default=1)
    parser.add_argument("--line-gap", type=int, default=1)
    parser.add_argument("--patch-multiplier", type=float, default=1.2)
    parser.add_argument("--output", type=Path, default=Path("rendered/reading-200"))
    args = parser.parse_args()

    if args.size <= 0:
        raise SystemExit("--size must be positive")
    if args.margin < 0 or args.line_gap < 0:
        raise SystemExit("margin and line gap must be non-negative")

    tasks = load_tasks(args.tasks)
    if len(tasks) != 200:
        raise SystemExit(f"expected exactly 200 tasks, found {len(tasks)}")

    available = installed_fonts()
    missing = [font_id for font_id in args.fonts if font_id not in available]
    if missing:
        raise SystemExit(f"fonts not installed: {', '.join(missing)}")

    args.output.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []

    for font_id in args.fonts:
        cfg = RenderConfig(
            font_id=font_id,
            font_size_px=args.size,
            line_gap_px=args.line_gap,
            margin_px=args.margin,
            max_aspect_ratio=None,
            patch_token_multiplier=args.patch_multiplier,
        )
        for task in tasks:
            out = args.output / font_id / f"{args.size}px" / f"{task.task_id}.png"
            result = render_instruction(task.instruction, out, cfg)
            records.append({
                "task_id": task.task_id,
                "category": task.category,
                "question": task.payload,
                "expected": task.expected,
                "scorer": task.scorer,
                "font_id": font_id,
                "font_family": available[font_id].get("family"),
                "is_control": font_id == CONTROL_FONT,
                "font_size_px": args.size,
                "margin_px": args.margin,
                "line_gap_px": args.line_gap,
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

    manifest_path = args.output / "manifest.jsonl"
    with manifest_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    summary = {
        "schema_version": 1,
        "tasks": len(tasks),
        "fonts": args.fonts,
        "candidate_fonts": [font for font in args.fonts if font != CONTROL_FONT],
        "control_font": CONTROL_FONT,
        "font_size_px": args.size,
        "images": len(records),
        "mean_patches": sum(float(r["patches"]) for r in records) / len(records),
        "mean_estimated_image_tokens": sum(float(r["estimated_image_tokens"]) for r in records) / len(records),
    }
    (args.output / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    expected = len(tasks) * len(args.fonts)
    pngs = list(args.output.rglob("*.png"))
    if len(records) != expected or len(pngs) != expected:
        raise SystemExit(
            f"render count mismatch: expected={expected} records={len(records)} pngs={len(pngs)}"
        )

    print(f"rendered {len(records)} images ({len(tasks)} passages × {len(args.fonts)} fonts)")
    print(f"manifest: {manifest_path}")
    print(f"mean patches: {summary['mean_patches']:.2f}")
    print(f"mean estimated image tokens: {summary['mean_estimated_image_tokens']:.2f}")


if __name__ == "__main__":
    main()
