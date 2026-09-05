#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys


def timestamped_run_dir(root: Path, started: datetime) -> Path:
    """Return runs/YYYY-MM-DD/HH-MM-SS.ffffffZ for one benchmark start."""
    started = started.astimezone(timezone.utc)
    date_dir = started.strftime("%Y-%m-%d")
    time_dir = started.strftime("%H-%M-%S.%fZ")
    return root / date_dir / time_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Start the fixed rendered-corpus benchmark in a UTC date/start-time directory, "
            "then delegate execution to scripts/run_rendered_corpus.py."
        )
    )
    parser.add_argument(
        "--runs-root",
        type=Path,
        default=Path("runs"),
        help="Root directory under which YYYY-MM-DD/HH-MM-SS.ffffffZ is created.",
    )
    parser.add_argument(
        "--resume",
        type=Path,
        help="Resume an existing exact run directory instead of creating a new timestamped directory.",
    )
    args, forwarded = parser.parse_known_args()

    command = [sys.executable, "scripts/run_rendered_corpus.py"]

    if args.resume is not None:
        command.extend(["--resume", str(args.resume)])
    else:
        started = datetime.now(timezone.utc)
        run_dir = timestamped_run_dir(args.runs_root, started)
        # run_rendered_corpus creates the final time directory with exist_ok=False.
        # Create only its date parent here.
        run_dir.parent.mkdir(parents=True, exist_ok=True)
        command.extend(["--output-dir", str(run_dir)])
        print(f"benchmark start UTC: {started.isoformat()}")
        print(f"run directory: {run_dir}")

    command.extend(forwarded)
    print("+", " ".join(command), flush=True)
    raise SystemExit(subprocess.run(command).returncode)


if __name__ == "__main__":
    main()
