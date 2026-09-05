#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import subprocess
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a font/size/spacing benchmark matrix sequentially.")
    parser.add_argument("config", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--codex-bin", default="codex")
    args = parser.parse_args()

    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    fonts = cfg["fonts"]
    sizes = cfg["sizes"]
    gaps = cfg.get("line_gaps", [1])

    failures = 0
    for font, size, gap in itertools.product(fonts, sizes, gaps):
        cmd = [
            sys.executable,
            "-m",
            "vce.run_cli",
            "--font",
            str(font),
            "--size",
            str(size),
            "--line-gap",
            str(gap),
            "--margin",
            str(cfg.get("margin", 1)),
            "--max-aspect",
            str(cfg.get("max_aspect", 2.0)),
            "--patch-multiplier",
            str(cfg.get("patch_multiplier", 1.2)),
            "--condition",
            str(cfg.get("condition", "both")),
            "--repetitions",
            str(cfg.get("repetitions", 1)),
            "--codex-bin",
            args.codex_bin,
        ]
        if "limit" in cfg and cfg["limit"] is not None:
            cmd.extend(["--limit", str(cfg["limit"])])
        if args.dry_run:
            cmd.append("--dry-run")

        print("+", " ".join(cmd), flush=True)
        result = subprocess.run(cmd)
        if result.returncode != 0:
            failures += 1
            print(f"matrix cell failed: font={font} size={size} gap={gap}", file=sys.stderr)

    if failures:
        raise SystemExit(f"{failures} matrix cells failed")


if __name__ == "__main__":
    main()
