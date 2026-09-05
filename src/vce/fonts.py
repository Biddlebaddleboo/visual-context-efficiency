from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INSTALLED = ROOT / "fonts" / "installed.json"


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def installed_fonts() -> dict[str, dict]:
    if not INSTALLED.exists():
        raise FileNotFoundError(
            f"{INSTALLED.relative_to(ROOT)} is missing. Run: python scripts/fetch_fonts.py"
        )
    data = json.loads(INSTALLED.read_text(encoding="utf-8"))
    return {item["id"]: item for item in data["fonts"]}


def resolve_font(font_id: str) -> tuple[Path, dict]:
    fonts = installed_fonts()
    if font_id not in fonts:
        raise KeyError(f"unknown font id {font_id!r}; installed: {', '.join(sorted(fonts))}")
    meta = fonts[font_id]
    path = ROOT / meta["path"]
    if not path.exists():
        raise FileNotFoundError(path)
    actual = file_sha256(path)
    expected = meta.get("sha256")
    if expected and actual != expected:
        raise RuntimeError(f"font hash changed for {font_id}: expected {expected}, got {actual}")
    return path, {**meta, "sha256": actual}
