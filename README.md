# Visual Context Efficiency

A public benchmark for measuring how efficiently **GPT-5.6 Luna** can understand and follow natural-language instructions when those instructions are rendered as images instead of supplied as text.

The project focuses on **semantic comprehension and instruction following**, not only character-perfect OCR. Natural-language context can recover from some glyph ambiguity that would make code, hashes, identifiers, or paths incorrect. The benchmark therefore asks a practical engineering question: how much visual compression can be applied before meaning or compliance degrades?

## Core research question

> How much can natural-language instructions be visually compressed before GPT-5.6 Luna's ability to understand and follow them degrades materially relative to the same instructions supplied as text?

The initial benchmark varies:

- font family;
- raster font size;
- line spacing;
- margins;
- image width and aspect ratio;
- wrapping and layout;
- 32×32 patch count; and
- instruction length and semantic complexity.

The optimization target is the **quality/token Pareto frontier**: configurations for which no lower-token configuration achieves equal or better instruction-following quality.

## Model scope

The initial research is intentionally limited to **GPT-5.6 Luna**. This is not a cross-model leaderboard. Restricting the model lets the experimental budget go toward typography, layout, task diversity, repetitions, and careful boundary testing.

## Lab architecture

A persistent **parent Codex session acts as the research coordinator**. It may formulate hypotheses, launch experiment batches, inspect aggregate results, investigate anomalies, and decide what to test next.

Every **scored observation** must be produced by a **fresh child Codex session** with no prior benchmark history.

```text
Parent Codex research coordinator
        |
        v
Python benchmark harness
  |     |     |     |
  v     v     v     v
fresh  fresh  fresh  fresh
child  child  child  child
Codex  Codex  Codex  Codex
  |     |     |     |
  +-----+-----+-----+
        |
        v
raw responses + deterministic scoring
        |
        v
aggregate results
        |
        v
Parent Codex reviews results and defines next experiment
```

The parent coordinator must **never directly answer a scored benchmark item**.

## Experimental conditions

Each task has an authoritative source instruction and, where practical, a machine-checkable expected result.

### Text baseline

A fresh child Codex session receives the original instruction as text plus the task payload.

### Image condition

A separate fresh child session receives a neutral wrapper such as:

> Follow the instructions in the image.

followed by the rendered instruction image and the same task payload.

The source instruction must **not** also be supplied as text in the image condition. It is retained only for rendering, hashing, scoring, and reproducibility.

## Primary metrics

The benchmark reports multiple dimensions rather than collapsing everything into OCR accuracy:

- task correctness;
- instruction compliance;
- negation accuracy;
- conditional-rule accuracy;
- structured-output compliance;
- hallucination / unsupported-value rate;
- exact-string accuracy for a smaller OCR-control subset;
- text-baseline-normalized accuracy;
- patch count and reported image input tokens; and
- semantic accuracy per input token.

A useful normalized metric is:

```text
visual_normalized_score = image_condition_score / text_baseline_score
```

## Initial typography sweep

Suggested initial font families:

- JetBrains Mono;
- Arial or Liberation Sans;
- Verdana;
- DejaVu Sans;
- Noto Sans;
- Atkinson Hyperlegible; and
- one readable serif control such as Georgia or Liberation Serif.

Suggested initial raster sizes:

- 8 px;
- 9 px;
- 10 px;
- 11 px;
- 12 px;
- 13 px;
- 14 px; and
- 16 px.

Initial rendering should otherwise stay deliberately simple and controlled: black text, white background, PNG, deterministic word wrapping, minimal margins, and a fixed line-gap policy.

## Staged study

1. **Harness validation** — prove clean-session isolation, image transport, response capture, scoring, and metadata collection.
2. **Typography screening** — approximately 30–40 representative tasks across the broad font/size grid.
3. **Focused validation** — approximately 150–200 tasks on the best 5–8 configurations, with repeated independent runs.
4. **Layout optimization** — line spacing, aspect ratio, margins, weight, and wrapping/layout strategies.
5. **Boundary confirmation** — dense testing near the smallest high-quality configuration to locate the practical failure cliff and confidence interval.

## Repository documents

- [`AGENTS.md`](AGENTS.md) — operating rules for the parent Codex coordinator.
- [`METHODOLOGY.md`](METHODOLOGY.md) — controls, metrics, scoring, statistics, and reproducibility.
- [`EXPERIMENT_PLAN.md`](EXPERIMENT_PLAN.md) — staged execution plan.
- [`BENCHMARK_TASKS.md`](BENCHMARK_TASKS.md) — task taxonomy and dataset requirements.
- [`RESEARCH_LOG.md`](RESEARCH_LOG.md) — contemporaneous research notebook template and first hypotheses.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution and reproducibility expectations.

Expected implementation directories later:

```text
benchmark/       Python orchestration, scoring, and Codex CLI integration
renderer/        deterministic instruction-image rendering
configs/         version-controlled experiment configurations
dataset/         synthetic benchmark tasks and schemas
runs/            raw run metadata and outputs
results/         aggregate tables and reports
experiments/     immutable experiment records
```

## Reproducibility

Every scored observation should be traceable to a task ID, dataset revision, source-instruction hash, condition, model identifier, fresh-session invocation, Codex CLI version where available, rendering parameters, output image hash, patch count, raw response, expected result, scoring rule, score breakdown, latency, process exit status, and retry metadata.

## Public-repo boundary

The benchmark methodology, synthetic datasets, renderer, harness, and aggregate results are intended to be public. Do not commit proprietary production prompts, credentials, customer information, private datasets, or unreleased business logic.

## Status

Planning and experimental-design phase. The benchmark harness and dataset are not yet implemented, and no empirical result should be described as established until it has been produced by a versioned experiment under this repository's methodology.
