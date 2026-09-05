# Reading-200 paired text/image benchmark report

Generated: `2026-09-05T16:27:29.181920+00:00`  
Run ID: `16-26-48.799642Z`  
Model: `gpt-5.6-luna`  
Codex CLI: `codex-cli 0.153.4`  
Dataset SHA-256: `987988ff39e3ed843ec1b6bb0b6287415c4cbfea83edf6ca4c60a7a25b6f1aef`  
Image manifest SHA-256: `60e10f54d4634514662be6b32f80c04d7f18e43fa535e3dee9cbe4e82e893a3e`

The dataset and PNG corpus are immutable committed inputs. Every observation used a fresh `codex exec --ephemeral` child session. Image observations supplied the passage only through the assigned PNG; text observations supplied the original passage as text. No text/image equivalence claim is made beyond these paired results.

## Completion and isolation

- Total observations: **6** (1,000 image + 200 text)
- Valid scored observations: **6**
- Final infrastructure failures: **0**
- Rows with infrastructure retries: **0**
- Unique child thread IDs: **6**

## Plain-text baseline

- Accuracy: **1/1 = 100.00%** (Wilson 95% CI 20.65%–100.00%)
- Mean latency: **3173 ms**
- Observed Codex input tokens: **13019.00 mean** (13019–13019, n=1)

## Image results by size

| Size | Passed/valid | Accuracy | Wilson 95% CI | Gap vs text | Mean patches | Mean est. image tokens | Mean latency ms |
|---|---|---|---|---|---|---|---|
| 8px | 1/1 | 100.00% | 20.65%–100.00% | +0.00% | 35.00 | 42.00 | 5782 |
| 9px | 1/1 | 100.00% | 20.65%–100.00% | +0.00% | 39.00 | 46.80 | 6070 |
| 10px | 1/1 | 100.00% | 20.65%–100.00% | +0.00% | 48.00 | 57.60 | 6456 |
| 11px | 1/1 | 100.00% | 20.65%–100.00% | +0.00% | 54.00 | 64.80 | 4917 |
| 12px | 1/1 | 100.00% | 20.65%–100.00% | +0.00% | 65.00 | 78.00 | 4247 |

Smallest size closest to text-baseline accuracy: **8px** (absolute gap 0.00%).

## Category accuracy

Text baseline:

| Category | Passed/valid | Accuracy | Wilson 95% CI |
|---|---|---|---|
| reading_fact | 1/1 | 100.00% | 20.65%–100.00% |

Image conditions:

| Size | Category | Passed/valid | Accuracy | Wilson 95% CI |
|---|---|---|---|---|
| 8px | reading_fact | 1/1 | 100.00% | 20.65%–100.00% |
| 9px | reading_fact | 1/1 | 100.00% | 20.65%–100.00% |
| 10px | reading_fact | 1/1 | 100.00% | 20.65%–100.00% |
| 11px | reading_fact | 1/1 | 100.00% | 20.65%–100.00% |
| 12px | reading_fact | 1/1 | 100.00% | 20.65%–100.00% |

Cause/location recovery from 8px to 12px:

Cause/location categories are not represented in this smoke subset.

## Task-by-task recovery from 8px to 12px

Recovered (8px fail → 12px pass): **0**; regressed: **0**; stable pass: **1**; stable fail: **0**.

| Task | Category | 8px | 12px | Delta |
|---|---|---|---|---|
| reading_001 | reading_fact | PASS | PASS | +0 |

## Accuracy-vs-image-token Pareto frontier

| Size | Accuracy | Mean est. image tokens | Mean patches |
|---|---|---|---|
| 8px | 100.00% | 42.00 | 35.00 |

## Infrastructure failures and retries

No final infrastructure failures were observed.
