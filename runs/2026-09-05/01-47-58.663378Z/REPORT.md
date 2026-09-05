# Visual Context Efficiency — rendered corpus benchmark report

Generated: `2026-09-05T02:23:47.699431+00:00`  
Run ID: `rendered-corpus-20260905T014758Z-088bf4c3`  
Model: `gpt-5.6-luna`  
Codex CLI: `codex-cli 0.152.1`  
Prompt template SHA-256: `80ceb0389039e724bd4d977e420fd33d37548ce05134cc02b27f00035205ebdb`

This report covers the fixed, pre-rendered instruction-image corpus. Each observation was produced by a fresh `codex exec --ephemeral` child session. The source instruction was not supplied as text; only the neutral wrapper, task payload, and corresponding instruction PNG were supplied to the child.

## Overall

- Observations: **1600**
- Valid model observations: **1600**
- Infrastructure failures: **0**
- Passed: **1412**
- Accuracy: **88.25%** (Wilson 95% CI 86.58%–89.74%)
- Mean 32×32 patches: **10.28**
- Mean estimated Luna image tokens: **12.33**
- Mean latency: **5359 ms**

## Coding vs non-coding

| Workload | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| coding | 800 | 680 | 85.00% | 82.36%–87.31% | 11.54 | 13.85 | 6.1387 | 5323 | 0 |
| noncoding | 800 | 732 | 91.50% | 89.36%–93.24% | 9.02 | 10.82 | 8.4558 | 5394 | 0 |

## By category

| Category | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| coding | 800 | 680 | 85.00% | 82.36%–87.31% | 11.54 | 13.85 | 6.1387 | 5323 | 0 |
| conditional | 120 | 115 | 95.83% | 90.62%–98.21% | 10.13 | 12.16 | 7.8810 | 5030 | 0 |
| formatting | 40 | 40 | 100.00% | 91.24%–100.00% | 8.60 | 10.32 | 9.6899 | 5086 | 0 |
| multi_step | 80 | 63 | 78.75% | 68.58%–86.29% | 10.25 | 12.30 | 6.4024 | 5334 | 0 |
| negation | 120 | 114 | 95.00% | 89.52%–97.69% | 8.30 | 9.96 | 9.5382 | 5161 | 0 |
| numeric_date | 80 | 76 | 95.00% | 87.84%–98.04% | 6.58 | 7.89 | 12.0406 | 5189 | 0 |
| ocr_control | 40 | 40 | 100.00% | 91.24%–100.00% | 8.80 | 10.56 | 9.4697 | 5794 | 0 |
| reference_resolution | 80 | 56 | 70.00% | 59.23%–78.94% | 8.93 | 10.71 | 6.5359 | 5489 | 0 |
| semantic_selection | 80 | 78 | 97.50% | 91.34%–99.31% | 5.78 | 6.93 | 14.0693 | 6871 | 0 |
| structured_output | 80 | 73 | 91.25% | 83.02%–95.70% | 9.85 | 11.82 | 7.7200 | 5098 | 0 |
| uncertainty | 80 | 77 | 96.25% | 89.55%–98.72% | 12.45 | 14.94 | 6.4424 | 5234 | 0 |

## By font

| Font | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| atkinson-hyperlegible | 320 | 280 | 87.50% | 83.43%–90.68% | 8.88 | 10.66 | 8.2102 | 5380 | 0 |
| fira-sans | 320 | 286 | 89.38% | 85.52%–92.30% | 10.58 | 12.69 | 7.0409 | 5109 | 0 |
| ibm-plex-sans | 320 | 284 | 88.75% | 84.82%–91.76% | 9.26 | 11.11 | 7.9874 | 5485 | 0 |
| jetbrains-mono | 320 | 281 | 87.81% | 83.77%–90.96% | 13.68 | 16.41 | 5.3512 | 5535 | 0 |
| source-sans-3 | 320 | 281 | 87.81% | 83.77%–90.96% | 9.00 | 10.80 | 8.1336 | 5285 | 0 |

## By font size

| Size px | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| 10 | 200 | 177 | 88.50% | 83.34%–92.21% | 7.75 | 9.29 | 9.5223 | 5413 | 0 |
| 11 | 200 | 176 | 88.00% | 82.77%–91.80% | 8.96 | 10.76 | 8.1800 | 5287 | 0 |
| 12 | 200 | 180 | 90.00% | 85.06%–93.43% | 9.98 | 11.98 | 7.5113 | 5161 | 0 |
| 13 | 200 | 175 | 87.50% | 82.20%–91.39% | 11.89 | 14.27 | 6.1300 | 5094 | 0 |
| 14 | 200 | 167 | 83.50% | 77.73%–88.00% | 13.56 | 16.27 | 5.1315 | 5141 | 0 |
| 16 | 200 | 179 | 89.50% | 84.48%–93.03% | 17.73 | 21.28 | 4.2054 | 5124 | 0 |
| 8 | 200 | 178 | 89.00% | 83.91%–92.62% | 5.74 | 6.89 | 12.9210 | 6361 | 0 |
| 9 | 200 | 180 | 90.00% | 85.06%–93.43% | 6.60 | 7.92 | 11.3636 | 5290 | 0 |

## By font × size

| Font | Size px | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|---|
| atkinson-hyperlegible | 10 | 40 | 36 | 90.00% | 76.95%–96.04% | 5.80 | 6.96 | 12.9310 | 5528 | 0 |
| atkinson-hyperlegible | 11 | 40 | 34 | 85.00% | 70.93%–92.94% | 8.18 | 9.81 | 8.6646 | 5292 | 0 |
| atkinson-hyperlegible | 12 | 40 | 37 | 92.50% | 80.14%–97.42% | 8.85 | 10.62 | 8.7100 | 5200 | 0 |
| atkinson-hyperlegible | 13 | 40 | 33 | 82.50% | 68.05%–91.25% | 10.43 | 12.51 | 6.5947 | 5093 | 0 |
| atkinson-hyperlegible | 14 | 40 | 34 | 85.00% | 70.93%–92.94% | 11.05 | 13.26 | 6.4103 | 5128 | 0 |
| atkinson-hyperlegible | 16 | 40 | 34 | 85.00% | 70.93%–92.94% | 16.60 | 19.92 | 4.2671 | 4927 | 0 |
| atkinson-hyperlegible | 8 | 40 | 36 | 90.00% | 76.95%–96.04% | 4.80 | 5.76 | 15.6250 | 6470 | 0 |
| atkinson-hyperlegible | 9 | 40 | 36 | 90.00% | 76.95%–96.04% | 5.35 | 6.42 | 14.0187 | 5406 | 0 |
| fira-sans | 10 | 40 | 38 | 95.00% | 83.50%–98.62% | 8.38 | 10.05 | 9.4527 | 5260 | 0 |
| fira-sans | 11 | 40 | 35 | 87.50% | 73.89%–94.54% | 9.15 | 10.98 | 7.9690 | 5181 | 0 |
| fira-sans | 12 | 40 | 36 | 90.00% | 76.95%–96.04% | 9.97 | 11.97 | 7.5188 | 4921 | 0 |
| fira-sans | 13 | 40 | 34 | 85.00% | 70.93%–92.94% | 10.85 | 13.02 | 6.5284 | 5042 | 0 |
| fira-sans | 14 | 40 | 35 | 87.50% | 73.89%–94.54% | 15.43 | 18.51 | 4.7272 | 4984 | 0 |
| fira-sans | 16 | 40 | 34 | 85.00% | 70.93%–92.94% | 17.52 | 21.03 | 4.0418 | 5108 | 0 |
| fira-sans | 8 | 40 | 38 | 95.00% | 83.50%–98.62% | 6.35 | 7.62 | 12.4672 | 4919 | 0 |
| fira-sans | 9 | 40 | 36 | 90.00% | 76.95%–96.04% | 6.97 | 8.37 | 10.7527 | 5458 | 0 |
| ibm-plex-sans | 10 | 40 | 35 | 87.50% | 73.89%–94.54% | 7.60 | 9.12 | 9.5943 | 5379 | 0 |
| ibm-plex-sans | 11 | 40 | 35 | 87.50% | 73.89%–94.54% | 8.22 | 9.87 | 8.8652 | 5331 | 0 |
| ibm-plex-sans | 12 | 40 | 37 | 92.50% | 80.14%–97.42% | 9.03 | 10.83 | 8.5411 | 5080 | 0 |
| ibm-plex-sans | 13 | 40 | 37 | 92.50% | 80.14%–97.42% | 10.68 | 12.81 | 7.2209 | 5066 | 0 |
| ibm-plex-sans | 14 | 40 | 31 | 77.50% | 62.50%–87.68% | 11.30 | 13.56 | 5.7153 | 5465 | 0 |
| ibm-plex-sans | 16 | 40 | 38 | 95.00% | 83.50%–98.62% | 16.90 | 20.28 | 4.6844 | 5327 | 0 |
| ibm-plex-sans | 8 | 40 | 34 | 85.00% | 70.93%–92.94% | 4.95 | 5.94 | 14.3098 | 6791 | 0 |
| ibm-plex-sans | 9 | 40 | 37 | 92.50% | 80.14%–97.42% | 5.40 | 6.48 | 14.2747 | 5438 | 0 |
| jetbrains-mono | 10 | 40 | 34 | 85.00% | 70.93%–92.94% | 9.82 | 11.79 | 7.2095 | 5484 | 0 |
| jetbrains-mono | 11 | 40 | 35 | 87.50% | 73.89%–94.54% | 10.85 | 13.02 | 6.7204 | 5196 | 0 |
| jetbrains-mono | 12 | 40 | 34 | 85.00% | 70.93%–92.94% | 12.97 | 15.57 | 5.4592 | 5144 | 0 |
| jetbrains-mono | 13 | 40 | 37 | 92.50% | 80.14%–97.42% | 17.62 | 21.15 | 4.3735 | 5334 | 0 |
| jetbrains-mono | 14 | 40 | 35 | 87.50% | 73.89%–94.54% | 19.38 | 23.25 | 3.7634 | 4948 | 0 |
| jetbrains-mono | 16 | 40 | 37 | 92.50% | 80.14%–97.42% | 21.93 | 26.31 | 3.5158 | 4999 | 0 |
| jetbrains-mono | 8 | 40 | 33 | 82.50% | 68.05%–91.25% | 8.00 | 9.60 | 8.5938 | 8055 | 0 |
| jetbrains-mono | 9 | 40 | 36 | 90.00% | 76.95%–96.04% | 8.82 | 10.59 | 8.4986 | 5116 | 0 |
| source-sans-3 | 10 | 40 | 34 | 85.00% | 70.93%–92.94% | 7.12 | 8.55 | 9.9415 | 5414 | 0 |
| source-sans-3 | 11 | 40 | 37 | 92.50% | 80.14%–97.42% | 8.43 | 10.11 | 9.1494 | 5433 | 0 |
| source-sans-3 | 12 | 40 | 36 | 90.00% | 76.95%–96.04% | 9.10 | 10.92 | 8.2418 | 5457 | 0 |
| source-sans-3 | 13 | 40 | 34 | 85.00% | 70.93%–92.94% | 9.90 | 11.88 | 7.1549 | 4934 | 0 |
| source-sans-3 | 14 | 40 | 32 | 80.00% | 65.24%–89.50% | 10.65 | 12.78 | 6.2598 | 5180 | 0 |
| source-sans-3 | 16 | 40 | 36 | 90.00% | 76.95%–96.04% | 15.72 | 18.87 | 4.7695 | 5256 | 0 |
| source-sans-3 | 8 | 40 | 37 | 92.50% | 80.14%–97.42% | 4.60 | 5.52 | 16.7572 | 5571 | 0 |
| source-sans-3 | 9 | 40 | 35 | 87.50% | 73.89%–94.54% | 6.45 | 7.74 | 11.3049 | 5030 | 0 |

## Empirical font×size Pareto frontier

| Font | Size px | Accuracy | Mean est. image tokens | Mean patches | Accuracy / 100 image tokens |
|---|---|---|---|---|---|
| source-sans-3 | 8 | 92.50% | 5.52 | 4.60 | 16.7572 |
| fira-sans | 8 | 95.00% | 7.62 | 6.35 | 12.4672 |

## Per-task robustness

| Task | Workload | Category | Valid | Pass | Accuracy | Mean est. image tokens |
|---|---|---|---|---|---|---|
| coding_009 | coding | coding | 40 | 0 | 0.00% | 15.36 |
| reference_002 | noncoding | reference_resolution | 40 | 27 | 67.50% | 10.20 |
| coding_014 | coding | coding | 40 | 28 | 70.00% | 14.58 |
| coding_016 | coding | coding | 40 | 29 | 72.50% | 13.35 |
| multistep_002 | noncoding | multi_step | 40 | 29 | 72.50% | 11.34 |
| reference_001 | noncoding | reference_resolution | 40 | 29 | 72.50% | 11.22 |
| coding_001 | coding | coding | 40 | 31 | 77.50% | 17.28 |
| coding_017 | coding | coding | 40 | 31 | 77.50% | 17.52 |
| coding_005 | coding | coding | 40 | 32 | 80.00% | 20.25 |
| coding_007 | coding | coding | 40 | 32 | 80.00% | 12.54 |
| structured_002 | noncoding | structured_output | 40 | 33 | 82.50% | 11.70 |
| multistep_001 | noncoding | multi_step | 40 | 34 | 85.00% | 13.26 |
| coding_002 | coding | coding | 40 | 35 | 87.50% | 15.54 |
| coding_012 | coding | coding | 40 | 35 | 87.50% | 12.27 |
| coding_019 | coding | coding | 40 | 35 | 87.50% | 14.40 |
| negation_003 | noncoding | negation | 40 | 35 | 87.50% | 11.61 |
| coding_015 | coding | coding | 40 | 36 | 90.00% | 11.94 |
| uncertainty_002 | noncoding | uncertainty | 40 | 37 | 92.50% | 14.16 |
| coding_003 | coding | coding | 40 | 38 | 95.00% | 14.19 |
| conditional_002 | noncoding | conditional | 40 | 38 | 95.00% | 12.69 |
| conditional_003 | noncoding | conditional | 40 | 38 | 95.00% | 12.45 |
| numeric_date_001 | noncoding | numeric_date | 40 | 38 | 95.00% | 6.18 |
| numeric_date_002 | noncoding | numeric_date | 40 | 38 | 95.00% | 9.60 |
| semantic_001 | noncoding | semantic_selection | 40 | 38 | 95.00% | 6.81 |
| coding_013 | coding | coding | 40 | 39 | 97.50% | 15.24 |
| coding_020 | coding | coding | 40 | 39 | 97.50% | 14.25 |
| conditional_001 | noncoding | conditional | 40 | 39 | 97.50% | 11.34 |
| negation_001 | noncoding | negation | 40 | 39 | 97.50% | 7.47 |
| coding_004 | coding | coding | 40 | 40 | 100.00% | 12.12 |
| coding_006 | coding | coding | 40 | 40 | 100.00% | 15.93 |
| coding_008 | coding | coding | 40 | 40 | 100.00% | 7.47 |
| coding_010 | coding | coding | 40 | 40 | 100.00% | 8.25 |
| coding_011 | coding | coding | 40 | 40 | 100.00% | 11.22 |
| coding_018 | coding | coding | 40 | 40 | 100.00% | 13.23 |
| formatting_001 | noncoding | formatting | 40 | 40 | 100.00% | 10.32 |
| negation_002 | noncoding | negation | 40 | 40 | 100.00% | 10.80 |
| ocr_control_001 | noncoding | ocr_control | 40 | 40 | 100.00% | 10.56 |
| semantic_002 | noncoding | semantic_selection | 40 | 40 | 100.00% | 7.05 |
| structured_001 | noncoding | structured_output | 40 | 40 | 100.00% | 11.94 |
| uncertainty_001 | noncoding | uncertainty | 40 | 40 | 100.00% | 15.72 |

## Model failures

There were **188** valid model responses that did not pass their deterministic scorer. The first 100 are listed below.

| Task | Font | Size px | Patches | Response |
|---|---|---|---|---|
| multistep_002 | atkinson-hyperlegible | 8 | 4 | 27 |
| numeric_date_002 | atkinson-hyperlegible | 8 | 4 | No such value |
| coding_001 | atkinson-hyperlegible | 8 | 7 | ```python ↩ def square(x): ↩     return x * x ↩ ``` |
| coding_009 | atkinson-hyperlegible | 8 | 6 | names.map(name => name.toUpperCase()) |
| numeric_date_002 | atkinson-hyperlegible | 9 | 4 | No such value. |
| coding_003 | atkinson-hyperlegible | 9 | 6 | ```8``` |
| coding_009 | atkinson-hyperlegible | 9 | 7 | names.map(name => name.toUpperCase()) |
| coding_016 | atkinson-hyperlegible | 9 | 6 | range(1, 4) |
| conditional_003 | atkinson-hyperlegible | 10 | 6 | UNKNOWN |
| structured_002 | atkinson-hyperlegible | 10 | 6 | {"NAME":"Delta","active":true} |
| coding_001 | atkinson-hyperlegible | 10 | 8 | ```python ↩ def square(x): ↩     return x * x ↩ ``` |
| coding_009 | atkinson-hyperlegible | 10 | 7 | names.map(name => name.toUpperCase()) |
| semantic_001 | atkinson-hyperlegible | 11 | 5 | Calgary |
| uncertainty_002 | atkinson-hyperlegible | 11 | 10 | tax |
| coding_001 | atkinson-hyperlegible | 11 | 12 | ```python ↩ def square(x): ↩     return x * x ↩ ``` |
| coding_009 | atkinson-hyperlegible | 11 | 10 | names.map(name => name.toUpperCase()) |
| coding_012 | atkinson-hyperlegible | 11 | 8 | ls -la |
| coding_020 | atkinson-hyperlegible | 11 | 10 | `git status` was run, but the environment returned a sandbox networking error before producing status output. |
| conditional_002 | atkinson-hyperlegible | 12 | 10 | true |
| reference_002 | atkinson-hyperlegible | 12 | 8 | Cole |
| coding_009 | atkinson-hyperlegible | 12 | 12 | names.map(name => name.toUpperCase()) |
| multistep_002 | atkinson-hyperlegible | 13 | 9 | 58 |
| reference_001 | atkinson-hyperlegible | 13 | 9 | 3.00 |
| coding_002 | atkinson-hyperlegible | 13 | 13 | ```javascript ↩ items.length ↩ ``` |
| coding_005 | atkinson-hyperlegible | 13 | 18 | WHERE active = 1 AND age >= 18 |
| coding_009 | atkinson-hyperlegible | 13 | 13 | ```javascript ↩ names.map(name => name.toUpperCase()) ↩ ``` |
| coding_012 | atkinson-hyperlegible | 13 | 10 | ls -la |
| coding_016 | atkinson-hyperlegible | 13 | 11 | ```python ↩ range(4) ↩ ``` |
| reference_002 | atkinson-hyperlegible | 14 | 9 | Cole |
| coding_007 | atkinson-hyperlegible | 14 | 11 | ```python ↩ if x > 0 and x % 2 == 0: ↩     print('match') ↩ ``` |
| coding_009 | atkinson-hyperlegible | 14 | 14 | ```javascript ↩ names.map(name => name.toUpperCase()) ↩ ``` |
| coding_014 | atkinson-hyperlegible | 14 | 14 | .notice { visibility: hidden; } |
| coding_017 | atkinson-hyperlegible | 14 | 16 | if (status === 'ready') { run(); } |
| coding_019 | atkinson-hyperlegible | 14 | 13 | ```python ↩ items[1:] ↩ ``` |
| structured_002 | atkinson-hyperlegible | 16 | 15 | {"name":"Delta","status":true} |
| coding_002 | atkinson-hyperlegible | 16 | 21 | ```javascript ↩ const count = items.length; ↩ ``` |
| coding_005 | atkinson-hyperlegible | 16 | 27 | status = 1 AND age >= 18 |
| coding_009 | atkinson-hyperlegible | 16 | 21 | `names.map(name => name.toUpperCase())` |
| coding_012 | atkinson-hyperlegible | 16 | 16 | ls -la |
| coding_016 | atkinson-hyperlegible | 16 | 18 | ```python ↩ for i in range(4): ↩     print(i) ↩ ``` |
| reference_002 | fira-sans | 8 | 6 | Ari |
| coding_009 | fira-sans | 8 | 8 | names.map(name => name.toUpperCase()) |
| negation_003 | fira-sans | 9 | 6 | 16.50 |
| multistep_002 | fira-sans | 9 | 6 | 18, 13, 27 |
| reference_001 | fira-sans | 9 | 6 | 3.00 |
| coding_009 | fira-sans | 9 | 8 | names.map(name => name.toUpperCase()) |
| coding_002 | fira-sans | 10 | 11 | ```javascript ↩ const count = items.length; ↩ ``` |
| coding_009 | fira-sans | 10 | 10 | names.map(name => name.toUpperCase()) |
| multistep_002 | fira-sans | 11 | 8 | 18, 13, 27 |
| coding_002 | fira-sans | 11 | 12 | ```javascript ↩ const count = items.length; ↩ ``` |
| coding_005 | fira-sans | 11 | 15 | active = 1 AND score >= 18 |
| coding_007 | fira-sans | 11 | 9 | ```python ↩ if x > 0 and x % 2 == 0: ↩     print('match') ↩ ``` |
| coding_009 | fira-sans | 11 | 11 | ```javascript ↩ names.map(name => name.toUpperCase()) ↩ ``` |
| multistep_002 | fira-sans | 12 | 9 | 58 |
| numeric_date_001 | fira-sans | 12 | 5 | 2025-12-31 |
| coding_009 | fira-sans | 12 | 12 | `names.map(name => name.toUpperCase())` |
| coding_017 | fira-sans | 12 | 15 | if (status === 'ready') { run(); } |
| reference_002 | fira-sans | 13 | 9 | Cole |
| coding_001 | fira-sans | 13 | 16 | ```python ↩ def square(x): ↩     return x * x ↩ ``` |
| coding_002 | fira-sans | 13 | 14 | ```javascript ↩ const count = items.length; ↩ ``` |
| coding_007 | fira-sans | 13 | 11 | ```python ↩ if x > 0 and x % 2 == 0: ↩     print('match') ↩ ``` |
| coding_009 | fira-sans | 13 | 13 | ```javascript ↩ names.map(name => name.toUpperCase()) ↩ ``` |
| coding_019 | fira-sans | 13 | 13 | ```python ↩ items[1:] ↩ ``` |
| structured_002 | fira-sans | 14 | 15 | {"name":"Delta","status":true} |
| reference_001 | fira-sans | 14 | 15 | 3.00 |
| coding_009 | fira-sans | 14 | 20 | names.map(name => name.toUpperCase()) |
| coding_014 | fira-sans | 14 | 18 | visibility: hidden; |
| coding_015 | fira-sans | 14 | 15 | Text before <br> text after |
| structured_002 | fira-sans | 16 | 15 | {"name":"Delta","status":"active"} |
| uncertainty_002 | fira-sans | 16 | 20 | Tax: Not shown; cannot be calculated from the total. |
| reference_002 | fira-sans | 16 | 14 | Cole |
| coding_007 | fira-sans | 16 | 18 | ```python ↩ if x > 0 and x % 2 == 0: ↩     print('match') ↩ ``` |
| coding_009 | fira-sans | 16 | 21 | `names.map(name => name.toUpperCase())` |
| coding_017 | fira-sans | 16 | 24 | ```javascript ↩ if (status === 'ready') { ↩   run(); ↩ } ↩ ``` |
| semantic_001 | ibm-plex-sans | 8 | 3 | Gulf of Saint Lawrence |
| conditional_003 | ibm-plex-sans | 8 | 5 | ERROR |
| reference_001 | ibm-plex-sans | 8 | 5 | 5.5 |
| coding_009 | ibm-plex-sans | 8 | 6 | names.map(name => name.toUpperCase()) |
| coding_014 | ibm-plex-sans | 8 | 6 | display:none |
| coding_019 | ibm-plex-sans | 8 | 6 | `items[1:]` |
| coding_001 | ibm-plex-sans | 9 | 8 | return x * x |
| coding_009 | ibm-plex-sans | 9 | 7 | names.map(name => name.toUpperCase()) |
| coding_014 | ibm-plex-sans | 9 | 6 | visibility: hidden; |
| multistep_001 | ibm-plex-sans | 10 | 8 | 4, 10, 18 |
| reference_001 | ibm-plex-sans | 10 | 7 | 3.00 |
| reference_002 | ibm-plex-sans | 10 | 6 | Dana |
| coding_005 | ibm-plex-sans | 10 | 12 | status = 1 AND age >= 18 |
| coding_009 | ibm-plex-sans | 10 | 9 | names.map(name => name.toUpperCase()) |
| negation_003 | ibm-plex-sans | 11 | 8 | A, B, D |
| reference_001 | ibm-plex-sans | 11 | 8 | 8.20 |
| reference_002 | ibm-plex-sans | 11 | 8 | Cole |
| coding_005 | ibm-plex-sans | 11 | 14 | ethnic = 1 AND age >= 18 |
| coding_009 | ibm-plex-sans | 11 | 10 | names.map(name => name.toUpperCase()) |
| coding_009 | ibm-plex-sans | 12 | 12 | names.map(name => name.toUpperCase()) |
| coding_016 | ibm-plex-sans | 12 | 10 | range(3) |
| coding_019 | ibm-plex-sans | 12 | 10 | [1:] |
| coding_009 | ibm-plex-sans | 13 | 13 | names.map(name => name.toUpperCase()) |
| coding_016 | ibm-plex-sans | 13 | 11 | ```python ↩ for i in range(4): ↩     print(i) ↩ ``` |
| coding_017 | ibm-plex-sans | 13 | 16 | if (status === 'ready') { run(); } |
| negation_003 | ibm-plex-sans | 14 | 11 | B |

## Infrastructure failures

No infrastructure failures were observed.

## Interpretation notes

- `estimated_image_tokens` uses the configured 1.2-token-per-32×32-patch estimate recorded by the renderer; it is an estimate, not a replacement for any usage fields reported by Codex/OpenAI.
- The Pareto frontier is descriptive for this exact task corpus and run. It treats higher accuracy and lower mean estimated image tokens as better; it is not a statistical equivalence test.
- Coding and non-coding results are shown separately because character-level damage can affect source-code-like instructions differently from redundant natural language.
- Infrastructure failures are excluded from accuracy denominators and retained separately in the raw results.
- `results.csv` is the flattened row-per-image analysis dataset. `results.jsonl` preserves substantially richer Codex event and scoring evidence.
