# Visual Context Efficiency — rendered corpus benchmark report

Generated: `2026-09-05T04:50:50.051386+00:00`  
Run ID: `rendered-corpus-20260905T045030Z-b5440af0`  
Model: `gpt-5.6-luna`  
Codex CLI: `codex-cli 0.152.1`  
Prompt template SHA-256: `d48ec730df5530e32f1eb5b52f259af4935db4e3c42c00ff395c2b17239c9af1`

This report covers the fixed, pre-rendered instruction-image corpus. Each observation was produced by a fresh `codex exec --ephemeral` child session. The source instruction was not supplied as text; only the neutral wrapper, task payload, and corresponding instruction PNG were supplied to the child.

## Overall

- Observations: **8**
- Valid model observations: **8**
- Infrastructure failures: **0**
- Passed: **6**
- Accuracy: **75.00%** (Wilson 95% CI 40.93%–92.85%)
- Mean 32×32 patches: **35.38**
- Mean estimated Luna image tokens: **42.45**
- Mean latency: **4767 ms**

## Coding vs non-coding

| Workload | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| noncoding | 8 | 6 | 75.00% | 40.93%–92.85% | 35.38 | 42.45 | 1.7668 | 4767 | 0 |

## By category

| Category | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| reading_cause | 1 | 0 | 0.00% | 0.00%–79.35% | 36.00 | 43.20 | 0.0000 | 3962 | 0 |
| reading_date | 2 | 2 | 100.00% | 34.24%–100.00% | 35.00 | 42.00 | 2.3810 | 6278 | 0 |
| reading_fact | 2 | 2 | 100.00% | 34.24%–100.00% | 35.50 | 42.60 | 2.3474 | 4102 | 0 |
| reading_location | 1 | 0 | 0.00% | 0.00%–79.35% | 35.00 | 42.00 | 0.0000 | 4705 | 0 |
| reading_quantity | 2 | 2 | 100.00% | 34.24%–100.00% | 35.50 | 42.60 | 2.3474 | 4352 | 0 |

## By font

| Font | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| fira-sans | 8 | 6 | 75.00% | 40.93%–92.85% | 35.38 | 42.45 | 1.7668 | 4767 | 0 |

## By font size

| Size px | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| 8 | 8 | 6 | 75.00% | 40.93%–92.85% | 35.38 | 42.45 | 1.7668 | 4767 | 0 |

## By font × size

| Font | Size px | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|---|
| fira-sans | 8 | 8 | 6 | 75.00% | 40.93%–92.85% | 35.38 | 42.45 | 1.7668 | 4767 | 0 |

## Empirical font×size Pareto frontier

| Font | Size px | Accuracy | Mean est. image tokens | Mean patches | Accuracy / 100 image tokens |
|---|---|---|---|---|---|
| fira-sans | 8 | 75.00% | 42.45 | 35.38 | 1.7668 |

## Per-task robustness

| Task | Workload | Category | Valid | Pass | Accuracy | Mean est. image tokens |
|---|---|---|---|---|---|---|
| reading_004 | noncoding | reading_cause | 1 | 0 | 0.00% | 43.20 |
| reading_005 | noncoding | reading_location | 1 | 0 | 0.00% | 42.00 |
| reading_001 | noncoding | reading_fact | 1 | 1 | 100.00% | 42.00 |
| reading_002 | noncoding | reading_date | 1 | 1 | 100.00% | 42.00 |
| reading_003 | noncoding | reading_quantity | 1 | 1 | 100.00% | 43.20 |
| reading_006 | noncoding | reading_fact | 1 | 1 | 100.00% | 43.20 |
| reading_007 | noncoding | reading_date | 1 | 1 | 100.00% | 42.00 |
| reading_008 | noncoding | reading_quantity | 1 | 1 | 100.00% | 42.00 |

## Model failures

There were **2** valid model responses that did not pass their deterministic scorer. The first 100 are listed below.

| Task | Font | Size px | Patches | Response |
|---|---|---|---|---|
| reading_004 | fira-sans | 8 | 36 | Because the inventory count took longer than expected. |
| reading_005 | fira-sans | 8 | 35 | The field station |

## Infrastructure failures

No infrastructure failures were observed.

## Interpretation notes

- `estimated_image_tokens` uses the configured 1.2-token-per-32×32-patch estimate recorded by the renderer; it is an estimate, not a replacement for any usage fields reported by Codex/OpenAI.
- The Pareto frontier is descriptive for this exact task corpus and run. It treats higher accuracy and lower mean estimated image tokens as better; it is not a statistical equivalence test.
- Coding and non-coding results are shown separately because character-level damage can affect source-code-like instructions differently from redundant natural language.
- Infrastructure failures are excluded from accuracy denominators and retained separately in the raw results.
- `results.csv` is the flattened row-per-image analysis dataset. `results.jsonl` preserves substantially richer Codex event and scoring evidence.
