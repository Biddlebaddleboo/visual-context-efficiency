#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    problems: list[str] = []

    if sys.version_info < (3, 11):
        problems.append(f"Python 3.11+ required; found {sys.version.split()[0]}")
    else:
        print(f"Python: {sys.version.split()[0]}")

    try:
        import PIL  # noqa: F401
        print("Pillow: installed")
    except ImportError:
        problems.append("Pillow missing; run: python -m pip install -e '.[dev]'")

    codex = shutil.which("codex")
    if not codex:
        problems.append("Codex CLI not found on PATH")
    else:
        proc = subprocess.run([codex, "--version"], capture_output=True, text=True, timeout=15)
        print("Codex:", (proc.stdout or proc.stderr).strip())

    installed = ROOT / "fonts" / "installed.json"
    if not installed.exists():
        problems.append("benchmark fonts not downloaded; run: python scripts/fetch_fonts.py")
    else:
        data = json.loads(installed.read_text(encoding="utf-8"))
        missing = [f["id"] for f in data.get("fonts", []) if not (ROOT / f["path"]).exists()]
        if missing:
            problems.append("missing downloaded fonts: " + ", ".join(missing))
        else:
            print(f"Fonts: {len(data.get('fonts', []))} installed")

    if problems:
        print("\nEnvironment is not ready:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        raise SystemExit(1)

    print("Environment looks ready.")


if __name__ == "__main__":
    main()
