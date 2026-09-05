#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "fonts" / "manifest.json"
OUT_DIR = ROOT / "fonts" / "files"
INSTALLED = ROOT / "fonts" / "installed.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def looks_like_font(data: bytes) -> bool:
    return len(data) > 10_000 and data[:4] in {b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1"}


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "visual-context-efficiency/0.1"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def main() -> None:
    parser = argparse.ArgumentParser(description="Download benchmark fonts and record exact SHA-256 hashes.")
    parser.add_argument("--force", action="store_true", help="Redownload existing files.")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    installed = {"schema_version": 1, "fonts": []}

    for item in manifest["fonts"]:
        path = OUT_DIR / item["filename"]
        if args.force or not path.exists():
            print(f"downloading {item['id']} ...")
            data = download(item["source"])
            if not looks_like_font(data):
                raise RuntimeError(f"download for {item['id']} does not look like a TTF/OTF font")
            path.write_bytes(data)
        digest = sha256(path)
        installed["fonts"].append({
            **item,
            "path": str(path.relative_to(ROOT)),
            "sha256": digest,
            "bytes": path.stat().st_size,
        })
        print(f"{item['id']}: {digest}")

    INSTALLED.write_text(json.dumps(installed, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {INSTALLED.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
