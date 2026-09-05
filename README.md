# Visual Context Efficiency

A public benchmark for measuring how efficiently **GPT-5.6 Luna** can understand and follow natural-language instructions when those instructions are rendered as images instead of supplied as text.

The project focuses on **semantic comprehension and instruction following**, not only character-perfect OCR. The practical question is:

> How much can natural-language instructions be visually compressed before GPT-5.6 Luna's ability to understand and follow them degrades materially relative to the same instructions supplied as text?

The optimization target is the **quality/token Pareto frontier**: configurations for which no lower-token visual representation achieves equal or better instruction-following quality.

## Scope

The initial benchmark is intentionally **GPT-5.6 Luna only**. It varies font family, raster size, line spacing, margins, wrapping/layout, aspect ratio, instruction length, semantic complexity, and 32×32 patch count.

The repository does not treat exact OCR as the headline metric. Exact identifiers and confusable characters are retained as a smaller control subset because natural-language instructions can often remain semantically recoverable after character-perfect OCR starts to degrade.

## Lab architecture

A persistent **parent Codex session acts as the research coordinator**. Every scored observation is produced by a **fresh child Codex CLI session**. The parent may design experiments and analyze results, but it must never directly answer scored benchmark items.

```text
Parent Codex coordinator
        |
        v
Python benchmark harness
        |
        +--> fresh Codex child -> one scored observation
        +--> fresh Codex child -> one scored observation
        +--> fresh Codex child -> one scored observation
        |
        v
raw JSONL + deterministic scoring + aggregate reports
```

The harness uses fresh `codex exec --ephemeral` invocations and does not use `resume` for scored trials.

## Quick start

Requirements:

- Python 3.11+
- Codex CLI installed and authenticated
- network access once to fetch the open-source benchmark fonts

Set up Python and fonts:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/fetch_fonts.py
python scripts/verify_environment.py
```

On Windows PowerShell, activate the virtual environment with `.venv\Scripts\Activate.ps1`.

Run the unit tests:

```bash
pytest
```

Render a few instruction images without calling Codex:

```bash
vce-render --font jetbrains-mono --size 14 --line-gap 1 --margin 1 --limit 4
```

Dry-run the paired benchmark path:

```bash
vce-run --font jetbrains-mono --size 14 --line-gap 1 --margin 1 --limit 4 --dry-run
```

Run a small real paired benchmark:

```bash
vce-run --font jetbrains-mono --size 14 --line-gap 1 --margin 1 --limit 4
```

Run a version-controlled matrix:

```bash
python scripts/run_matrix.py configs/smoke.json --dry-run
python scripts/run_matrix.py configs/smoke.json
```

The broader first-pass matrix is in `configs/screening.json`.

## Fonts

The initial font set is deliberately open-source:

- JetBrains Mono
- Atkinson Hyperlegible
- Source Sans 3
- IBM Plex Sans
- Fira Sans

Font binaries are downloaded by `scripts/fetch_fonts.py` rather than committed. The script writes `fonts/installed.json` containing the exact SHA-256 of every downloaded font. Each scored image observation records the font hash again, so published results can identify the exact font bytes used.

## Paired conditions

### Text baseline

A fresh child receives the authoritative instruction as text plus the task payload.

### Image condition

A different fresh child receives only a neutral wrapper such as `Follow the instructions in the attached image.`, the rendered instruction image, and the same task payload. The authoritative instruction is **not duplicated as text**.

## Rendering

The renderer is deterministic for a given source instruction and configuration. It records:

- font ID and SHA-256;
- raster font size;
- line gap and margin;
- rendered dimensions;
- line count and line-box height;
- image SHA-256;
- 32×32 patch grid;
- total patch count; and
- estimated image tokens using the configured patch multiplier.

The default renderer searches widths and chooses the lowest-patch layout subject to a practical aspect-ratio constraint. Aspect ratio is itself configurable for later experiments.

## Benchmark data

`dataset/tasks.jsonl` contains a small seed dataset for harness validation. It covers semantic selection, negation, conditional rules, multi-step instructions, JSON output, null behavior, date comparison, formatting, reference resolution, and an exact-character OCR control.

The planned validation set is substantially larger; see [`BENCHMARK_TASKS.md`](BENCHMARK_TASKS.md).

## Results

Each `vce-run` invocation creates an immutable-style run directory under `runs/<run-id>/` containing:

```text
config.json
images/             # for image conditions
results.jsonl       # raw observation records + scores
```

Infrastructure failures are separated from model failures. Valid model responses are never silently retried just because they score poorly.

Summarize a run with:

```bash
vce-report runs/<run-id>/results.jsonl
```

## Repository documents

- [`AGENTS.md`](AGENTS.md) — rules for the parent Codex research coordinator.
- [`METHODOLOGY.md`](METHODOLOGY.md) — controls, metrics, scoring, statistics, and reproducibility.
- [`EXPERIMENT_PLAN.md`](EXPERIMENT_PLAN.md) — staged execution plan.
- [`BENCHMARK_TASKS.md`](BENCHMARK_TASKS.md) — task taxonomy and dataset requirements.
- [`RESEARCH_LOG.md`](RESEARCH_LOG.md) — contemporaneous research notebook.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution and reproducibility expectations.

## Public-repo boundary

Use synthetic or clearly redistributable benchmark content. Do not commit API keys, customer data, proprietary production prompts, private datasets, or unreleased business logic.

## Status

The initial Python harness, deterministic renderer, font fetcher, fresh Codex CLI child runner, seed dataset, scorers, matrix driver, and report utility are implemented. The current seed tasks are for harness validation, not a final empirical benchmark result.
