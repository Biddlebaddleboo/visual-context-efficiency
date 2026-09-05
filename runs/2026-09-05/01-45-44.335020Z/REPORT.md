# Visual Context Efficiency — rendered corpus benchmark report

Generated: `2026-09-05T01:45:45.445247+00:00`  
Run ID: `rendered-corpus-20260905T014544Z-58786068`  
Model: `gpt-5.6-luna`  
Codex CLI: `codex-cli 0.152.1`  
Prompt template SHA-256: `80ceb0389039e724bd4d977e420fd33d37548ce05134cc02b27f00035205ebdb`

This report covers the fixed, pre-rendered instruction-image corpus. Each observation was produced by a fresh `codex exec --ephemeral` child session. The source instruction was not supplied as text; only the neutral wrapper, task payload, and corresponding instruction PNG were supplied to the child.

## Overall

- Observations: **8**
- Valid model observations: **0**
- Infrastructure failures: **8**
- Passed: **0**
- Accuracy: **0.00%** (Wilson 95% CI 0.00%–0.00%)
- Mean 32×32 patches: **0.00**
- Mean estimated Luna image tokens: **0.00**
- Mean latency: **0 ms**

## Coding vs non-coding

| Workload | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| noncoding | 0 | 0 | 0.00% | 0.00%–0.00% | 0.00 | 0.00 | 0.0000 | 0 | 8 |

## By category

| Category | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| conditional | 0 | 0 | 0.00% | 0.00%–0.00% | 0.00 | 0.00 | 0.0000 | 0 | 3 |
| negation | 0 | 0 | 0.00% | 0.00%–0.00% | 0.00 | 0.00 | 0.0000 | 0 | 3 |
| semantic_selection | 0 | 0 | 0.00% | 0.00%–0.00% | 0.00 | 0.00 | 0.0000 | 0 | 2 |

## By font

| Font | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| atkinson-hyperlegible | 0 | 0 | 0.00% | 0.00%–0.00% | 0.00 | 0.00 | 0.0000 | 0 | 8 |

## By font size

| Size px | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| 8 | 0 | 0 | 0.00% | 0.00%–0.00% | 0.00 | 0.00 | 0.0000 | 0 | 8 |

## By font × size

| Font | Size px | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|---|
| atkinson-hyperlegible | 8 | 0 | 0 | 0.00% | 0.00%–0.00% | 0.00 | 0.00 | 0.0000 | 0 | 8 |

## Empirical font×size Pareto frontier

No valid configurations were available.

## Per-task robustness

| Task | Workload | Category | Valid | Pass | Accuracy | Mean est. image tokens |
|---|---|---|---|---|---|---|
| conditional_001 | noncoding | conditional | 0 | 0 | 0.00% | 0.00 |
| conditional_002 | noncoding | conditional | 0 | 0 | 0.00% | 0.00 |
| conditional_003 | noncoding | conditional | 0 | 0 | 0.00% | 0.00 |
| negation_001 | noncoding | negation | 0 | 0 | 0.00% | 0.00 |
| negation_002 | noncoding | negation | 0 | 0 | 0.00% | 0.00 |
| negation_003 | noncoding | negation | 0 | 0 | 0.00% | 0.00 |
| semantic_001 | noncoding | semantic_selection | 0 | 0 | 0.00% | 0.00 |
| semantic_002 | noncoding | semantic_selection | 0 | 0 | 0.00% | 0.00 |

## Model failures

No valid model failures were observed.

## Infrastructure failures

| Reason | Count |
|---|---|
| codex_nonzero_exit | 8 |

## Interpretation notes

- `estimated_image_tokens` uses the configured 1.2-token-per-32×32-patch estimate recorded by the renderer; it is an estimate, not a replacement for any usage fields reported by Codex/OpenAI.
- The Pareto frontier is descriptive for this exact task corpus and run. It treats higher accuracy and lower mean estimated image tokens as better; it is not a statistical equivalence test.
- Coding and non-coding results are shown separately because character-level damage can affect source-code-like instructions differently from redundant natural language.
- Infrastructure failures are excluded from accuracy denominators and retained separately in the raw results.
- `results.csv` is the flattened row-per-image analysis dataset. `results.jsonl` preserves substantially richer Codex event and scoring evidence.
