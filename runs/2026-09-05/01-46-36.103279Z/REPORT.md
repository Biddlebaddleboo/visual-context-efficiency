# Visual Context Efficiency — rendered corpus benchmark report

Generated: `2026-09-05T01:47:08.184795+00:00`  
Run ID: `rendered-corpus-20260905T014636Z-c0751719`  
Model: `gpt-5.6-luna`  
Codex CLI: `codex-cli 0.152.1`  
Prompt template SHA-256: `80ceb0389039e724bd4d977e420fd33d37548ce05134cc02b27f00035205ebdb`

This report covers the fixed, pre-rendered instruction-image corpus. Each observation was produced by a fresh `codex exec --ephemeral` child session. The source instruction was not supplied as text; only the neutral wrapper, task payload, and corresponding instruction PNG were supplied to the child.

## Overall

- Observations: **8**
- Valid model observations: **8**
- Infrastructure failures: **0**
- Passed: **7**
- Accuracy: **87.50%** (Wilson 95% CI 52.91%–97.76%)
- Mean 32×32 patches: **4.00**
- Mean estimated Luna image tokens: **4.80**
- Mean latency: **7468 ms**

## Coding vs non-coding

| Workload | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| noncoding | 8 | 7 | 87.50% | 52.91%–97.76% | 4.00 | 4.80 | 18.2292 | 7468 | 0 |

## By category

| Category | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| conditional | 3 | 3 | 100.00% | 43.85%–100.00% | 4.67 | 5.60 | 17.8571 | 6902 | 0 |
| negation | 3 | 3 | 100.00% | 43.85%–100.00% | 4.00 | 4.80 | 20.8333 | 6620 | 0 |
| semantic_selection | 2 | 1 | 50.00% | 9.45%–90.55% | 3.00 | 3.60 | 13.8889 | 9589 | 0 |

## By font

| Font | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| atkinson-hyperlegible | 8 | 7 | 87.50% | 52.91%–97.76% | 4.00 | 4.80 | 18.2292 | 7468 | 0 |

## By font size

| Size px | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| 8 | 8 | 7 | 87.50% | 52.91%–97.76% | 4.00 | 4.80 | 18.2292 | 7468 | 0 |

## By font × size

| Font | Size px | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|---|
| atkinson-hyperlegible | 8 | 8 | 7 | 87.50% | 52.91%–97.76% | 4.00 | 4.80 | 18.2292 | 7468 | 0 |

## Empirical font×size Pareto frontier

| Font | Size px | Accuracy | Mean est. image tokens | Mean patches | Accuracy / 100 image tokens |
|---|---|---|---|---|---|
| atkinson-hyperlegible | 8 | 87.50% | 4.80 | 4.00 | 18.2292 |

## Per-task robustness

| Task | Workload | Category | Valid | Pass | Accuracy | Mean est. image tokens |
|---|---|---|---|---|---|---|
| semantic_001 | noncoding | semantic_selection | 1 | 0 | 0.00% | 3.60 |
| conditional_001 | noncoding | conditional | 1 | 1 | 100.00% | 4.80 |
| conditional_002 | noncoding | conditional | 1 | 1 | 100.00% | 6.00 |
| conditional_003 | noncoding | conditional | 1 | 1 | 100.00% | 6.00 |
| negation_001 | noncoding | negation | 1 | 1 | 100.00% | 3.60 |
| negation_002 | noncoding | negation | 1 | 1 | 100.00% | 4.80 |
| negation_003 | noncoding | negation | 1 | 1 | 100.00% | 6.00 |
| semantic_002 | noncoding | semantic_selection | 1 | 1 | 100.00% | 3.60 |

## Model failures

There were **1** valid model responses that did not pass their deterministic scorer. The first 100 are listed below.

| Task | Font | Size px | Patches | Response |
|---|---|---|---|---|
| semantic_001 | atkinson-hyperlegible | 8 | 3 | Pacific Ocean, Vancouver |

## Infrastructure failures

No infrastructure failures were observed.

## Interpretation notes

- `estimated_image_tokens` uses the configured 1.2-token-per-32×32-patch estimate recorded by the renderer; it is an estimate, not a replacement for any usage fields reported by Codex/OpenAI.
- The Pareto frontier is descriptive for this exact task corpus and run. It treats higher accuracy and lower mean estimated image tokens as better; it is not a statistical equivalence test.
- Coding and non-coding results are shown separately because character-level damage can affect source-code-like instructions differently from redundant natural language.
- Infrastructure failures are excluded from accuracy denominators and retained separately in the raw results.
- `results.csv` is the flattened row-per-image analysis dataset. `results.jsonl` preserves substantially richer Codex event and scoring evidence.
