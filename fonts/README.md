# Benchmark Fonts

This repository does not commit font binaries. `scripts/fetch_fonts.py` downloads the open-source benchmark fonts declared in `manifest.json` into `fonts/files/` and writes `fonts/installed.json` containing SHA-256 hashes of the exact downloaded files.

The initial set intentionally uses redistributable/open-source fonts so anyone can reproduce the benchmark without depending on proprietary Microsoft fonts.

Run:

```bash
python scripts/fetch_fonts.py
```

The renderer refers to fonts by the stable IDs in `manifest.json`, for example `jetbrains-mono` or `source-sans-3`.

For reproducible published runs, preserve the generated `installed.json` alongside the run metadata so the exact font bytes can be identified even if an upstream repository later changes.

Font licensing remains governed by each upstream project. The manifest records the expected license family and source location; it is not a substitute for the upstream license text.
