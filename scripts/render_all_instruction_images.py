#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from vce.dataset import load_tasks
from vce.fonts import installed_fonts
from vce.render import RenderConfig, render_instruction


def parse_sizes(value: str) -> list[int]:
    sizes = [int(part.strip()) for part in value.split(",") if part.strip()]
    if not sizes:
        raise argparse.ArgumentTypeError("at least one font size is required")
    if any(size <= 0 for size in sizes):
        raise argparse.ArgumentTypeError("font sizes must be positive integers")
    return sizes


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Render every benchmark instruction for every installed font and requested size, "
            "minimizing 32x32 patch count first and square-distance second."
        )
    )
    parser.add_argument("--tasks", type=Path, default=Path("dataset/tasks.jsonl"))
    parser.add_argument("--sizes", type=parse_sizes, default=parse_sizes("8,9,10,11,12,13,14,16"))
    parser.add_argument("--margin", type=int, default=1)
    parser.add_argument("--line-gap", type=int, default=1)
    parser.add_argument("--patch-multiplier", type=float, default=1.2)
    parser.add_argument("--output", type=Path, default=Path("rendered/all-instructions"))
    args = parser.parse_args()

    if args.margin < 0 or args.line_gap < 0:
        parser.error("margin and line gap must be non-negative")

    tasks = load_tasks(args.tasks)
    fonts = installed_fonts()
    args.output.mkdir(parents=True, exist_ok=True)

    manifest_path = args.output / "manifest.jsonl"
    summary_path = args.output / "SUMMARY.md"
    records: list[dict] = []

    for font_id in sorted(fonts):
        for size in args.sizes:
            cfg = RenderConfig(
                font_id=font_id,
                font_size_px=size,
                line_gap_px=args.line_gap,
                margin_px=args.margin,
                # Search the full configured patch-column range without imposing
                # an aspect-ratio cutoff. render._layout ranks candidates
                # lexicographically by: (1) patch count, (2) square distance,
                # (3) raw pixel area. This therefore gives the globally lowest
                # 32x32 patch count available to the renderer, with the most
                # square layout chosen among equal-patch candidates.
                max_aspect_ratio=None,
                patch_token_multiplier=args.patch_multiplier,
            )

            for task in tasks:
                out = args.output / font_id / f"{size}px" / f"{task.task_id}.png"
                result = render_instruction(task.instruction, out, cfg)
                record = {
                    "task_id": task.task_id,
                    "category": task.category,
                    "instruction": task.instruction,
                    "font_id": font_id,
                    "font_family": fonts[font_id].get("family"),
                    "font_size_px": size,
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
                }
                records.append(record)

    with manifest_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    grouped: dict[tuple[str, int], list[dict]] = {}
    for record in records:
        grouped.setdefault((record["font_id"], record["font_size_px"]), []).append(record)

    lines = [
        "# Rendered instruction image summary",
        "",
        f"Tasks: **{len(tasks)}**  ",
        f"Fonts: **{len(fonts)}**  ",
        f"Sizes: **{', '.join(str(x) + 'px' for x in args.sizes)}**  ",
        f"Images: **{len(records)}**",
        "",
        "Every image uses a 1 px margin and 1 px line gap by default. Layout selection minimizes total 32x32 patches first, then minimizes distance from a square among equal-patch layouts, then minimizes raw pixel area.",
        "",
        "| Font | Size | Images | Avg patches | Min | Max | Avg est. Luna image tokens |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for (font_id, size), items in sorted(grouped.items()):
        patch_values = [item["patches"] for item in items]
        token_values = [item["estimated_image_tokens"] for item in items]
        lines.append(
            f"| {font_id} | {size}px | {len(items)} | "
            f"{sum(patch_values) / len(patch_values):.2f} | {min(patch_values)} | {max(patch_values)} | "
            f"{sum(token_values) / len(token_values):.2f} |"
        )
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"rendered {len(records)} images")
    print(f"manifest: {manifest_path}")
    print(f"summary: {summary_path}")


if __name__ == "__main__":
    main()
