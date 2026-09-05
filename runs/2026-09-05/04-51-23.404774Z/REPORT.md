# Visual Context Efficiency — rendered corpus benchmark report

Generated: `2026-09-05T05:47:00.427293+00:00`  
Run ID: `rendered-corpus-20260905T045123Z-20ada5a7`  
Model: `gpt-5.6-luna`  
Codex CLI: `codex-cli 0.152.1`  
Prompt template SHA-256: `d48ec730df5530e32f1eb5b52f259af4935db4e3c42c00ff395c2b17239c9af1`

This report covers the fixed, pre-rendered instruction-image corpus. Each observation was produced by a fresh `codex exec --ephemeral` child session. The source instruction was not supplied as text; only the neutral wrapper, task payload, and corresponding instruction PNG were supplied to the child.

## Overall

- Observations: **1400**
- Valid model observations: **1400**
- Infrastructure failures: **0**
- Passed: **612**
- Accuracy: **43.71%** (Wilson 95% CI 41.14%–46.33%)
- Mean 32×32 patches: **33.29**
- Mean estimated Luna image tokens: **39.95**
- Mean latency: **9271 ms**

## Coding vs non-coding

| Workload | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| noncoding | 1400 | 612 | 43.71% | 41.14%–46.33% | 33.29 | 39.95 | 1.0943 | 9271 | 0 |

## By category

| Category | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| reading_cause | 280 | 0 | 0.00% | 0.00%–1.35% | 33.79 | 40.55 | 0.0000 | 10704 | 0 |
| reading_date | 280 | 233 | 83.21% | 78.39%–87.14% | 32.47 | 38.97 | 2.1356 | 9188 | 0 |
| reading_fact | 280 | 199 | 71.07% | 65.50%–76.07% | 33.35 | 40.02 | 1.7759 | 10366 | 0 |
| reading_location | 280 | 6 | 2.14% | 0.99%–4.60% | 33.68 | 40.41 | 0.0530 | 8562 | 0 |
| reading_quantity | 280 | 174 | 62.14% | 56.33%–67.62% | 33.15 | 39.78 | 1.5620 | 7533 | 0 |

## By font

| Font | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| atkinson-hyperlegible | 200 | 67 | 33.50% | 27.32%–40.30% | 25.61 | 30.73 | 1.0901 | 12059 | 0 |
| fira-sans | 200 | 106 | 53.00% | 46.09%–59.80% | 35.30 | 42.37 | 1.2510 | 7337 | 0 |
| ibm-plex-sans | 200 | 75 | 37.50% | 31.09%–44.39% | 30.32 | 36.38 | 1.0307 | 10007 | 0 |
| inter | 200 | 103 | 51.50% | 44.61%–58.33% | 39.15 | 46.97 | 1.0964 | 6604 | 0 |
| jetbrains-mono | 200 | 108 | 54.00% | 47.08%–60.77% | 45.43 | 54.52 | 0.9905 | 5392 | 0 |
| noto-sans | 200 | 70 | 35.00% | 28.73%–41.84% | 31.96 | 38.36 | 0.9125 | 10886 | 0 |
| source-sans-3 | 200 | 83 | 41.50% | 34.89%–48.43% | 25.25 | 30.30 | 1.3696 | 12610 | 0 |

## By font size

| Size px | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|
| 8 | 1400 | 612 | 43.71% | 41.14%–46.33% | 33.29 | 39.95 | 1.0943 | 9271 | 0 |

## By font × size

| Font | Size px | Valid | Pass | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens | Accuracy / 100 image tokens | Mean latency ms | Infra failures |
|---|---|---|---|---|---|---|---|---|---|---|
| atkinson-hyperlegible | 8 | 200 | 67 | 33.50% | 27.32%–40.30% | 25.61 | 30.73 | 1.0901 | 12059 | 0 |
| fira-sans | 8 | 200 | 106 | 53.00% | 46.09%–59.80% | 35.30 | 42.37 | 1.2510 | 7337 | 0 |
| ibm-plex-sans | 8 | 200 | 75 | 37.50% | 31.09%–44.39% | 30.32 | 36.38 | 1.0307 | 10007 | 0 |
| inter | 8 | 200 | 103 | 51.50% | 44.61%–58.33% | 39.15 | 46.97 | 1.0964 | 6604 | 0 |
| jetbrains-mono | 8 | 200 | 108 | 54.00% | 47.08%–60.77% | 45.43 | 54.52 | 0.9905 | 5392 | 0 |
| noto-sans | 8 | 200 | 70 | 35.00% | 28.73%–41.84% | 31.96 | 38.36 | 0.9125 | 10886 | 0 |
| source-sans-3 | 8 | 200 | 83 | 41.50% | 34.89%–48.43% | 25.25 | 30.30 | 1.3696 | 12610 | 0 |

## Empirical font×size Pareto frontier

| Font | Size px | Accuracy | Mean est. image tokens | Mean patches | Accuracy / 100 image tokens |
|---|---|---|---|---|---|
| source-sans-3 | 8 | 41.50% | 30.30 | 25.25 | 1.3696 |
| fira-sans | 8 | 53.00% | 42.37 | 35.30 | 1.2510 |
| jetbrains-mono | 8 | 54.00% | 54.52 | 45.43 | 0.9905 |

## Per-task robustness

| Task | Workload | Category | Valid | Pass | Accuracy | Mean est. image tokens |
|---|---|---|---|---|---|---|
| reading_004 | noncoding | reading_cause | 7 | 0 | 0.00% | 41.66 |
| reading_005 | noncoding | reading_location | 7 | 0 | 0.00% | 39.94 |
| reading_009 | noncoding | reading_cause | 7 | 0 | 0.00% | 40.80 |
| reading_010 | noncoding | reading_location | 7 | 0 | 0.00% | 38.57 |
| reading_014 | noncoding | reading_cause | 7 | 0 | 0.00% | 40.97 |
| reading_015 | noncoding | reading_location | 7 | 0 | 0.00% | 41.31 |
| reading_019 | noncoding | reading_cause | 7 | 0 | 0.00% | 42.51 |
| reading_020 | noncoding | reading_location | 7 | 0 | 0.00% | 40.29 |
| reading_024 | noncoding | reading_cause | 7 | 0 | 0.00% | 39.26 |
| reading_029 | noncoding | reading_cause | 7 | 0 | 0.00% | 42.86 |
| reading_030 | noncoding | reading_location | 7 | 0 | 0.00% | 41.66 |
| reading_034 | noncoding | reading_cause | 7 | 0 | 0.00% | 40.29 |
| reading_035 | noncoding | reading_location | 7 | 0 | 0.00% | 39.26 |
| reading_039 | noncoding | reading_cause | 7 | 0 | 0.00% | 39.94 |
| reading_040 | noncoding | reading_location | 7 | 0 | 0.00% | 39.94 |
| reading_044 | noncoding | reading_cause | 7 | 0 | 0.00% | 39.94 |
| reading_045 | noncoding | reading_location | 7 | 0 | 0.00% | 40.29 |
| reading_049 | noncoding | reading_cause | 7 | 0 | 0.00% | 40.29 |
| reading_050 | noncoding | reading_location | 7 | 0 | 0.00% | 39.60 |
| reading_054 | noncoding | reading_cause | 7 | 0 | 0.00% | 39.60 |
| reading_059 | noncoding | reading_cause | 7 | 0 | 0.00% | 38.57 |
| reading_060 | noncoding | reading_location | 7 | 0 | 0.00% | 42.69 |
| reading_064 | noncoding | reading_cause | 7 | 0 | 0.00% | 41.49 |
| reading_065 | noncoding | reading_location | 7 | 0 | 0.00% | 41.49 |
| reading_069 | noncoding | reading_cause | 7 | 0 | 0.00% | 41.66 |
| reading_070 | noncoding | reading_location | 7 | 0 | 0.00% | 42.00 |
| reading_074 | noncoding | reading_cause | 7 | 0 | 0.00% | 41.49 |
| reading_075 | noncoding | reading_location | 7 | 0 | 0.00% | 39.26 |
| reading_079 | noncoding | reading_cause | 7 | 0 | 0.00% | 40.80 |
| reading_084 | noncoding | reading_cause | 7 | 0 | 0.00% | 37.37 |
| reading_085 | noncoding | reading_location | 7 | 0 | 0.00% | 40.11 |
| reading_089 | noncoding | reading_cause | 7 | 0 | 0.00% | 41.14 |
| reading_090 | noncoding | reading_location | 7 | 0 | 0.00% | 42.00 |
| reading_094 | noncoding | reading_cause | 7 | 0 | 0.00% | 42.51 |
| reading_099 | noncoding | reading_cause | 7 | 0 | 0.00% | 39.94 |
| reading_100 | noncoding | reading_location | 7 | 0 | 0.00% | 39.77 |
| reading_104 | noncoding | reading_cause | 7 | 0 | 0.00% | 41.14 |
| reading_109 | noncoding | reading_cause | 7 | 0 | 0.00% | 38.57 |
| reading_114 | noncoding | reading_cause | 7 | 0 | 0.00% | 38.91 |
| reading_115 | noncoding | reading_location | 7 | 0 | 0.00% | 38.57 |
| reading_119 | noncoding | reading_cause | 7 | 0 | 0.00% | 40.97 |
| reading_120 | noncoding | reading_location | 7 | 0 | 0.00% | 42.00 |
| reading_124 | noncoding | reading_cause | 7 | 0 | 0.00% | 42.51 |
| reading_125 | noncoding | reading_location | 7 | 0 | 0.00% | 41.49 |
| reading_129 | noncoding | reading_cause | 7 | 0 | 0.00% | 40.63 |
| reading_130 | noncoding | reading_location | 7 | 0 | 0.00% | 38.74 |
| reading_134 | noncoding | reading_cause | 7 | 0 | 0.00% | 39.09 |
| reading_135 | noncoding | reading_location | 7 | 0 | 0.00% | 43.20 |
| reading_139 | noncoding | reading_cause | 7 | 0 | 0.00% | 40.46 |
| reading_140 | noncoding | reading_location | 7 | 0 | 0.00% | 40.63 |
| reading_144 | noncoding | reading_cause | 7 | 0 | 0.00% | 42.51 |
| reading_145 | noncoding | reading_location | 7 | 0 | 0.00% | 38.57 |
| reading_149 | noncoding | reading_cause | 7 | 0 | 0.00% | 42.17 |
| reading_150 | noncoding | reading_location | 7 | 0 | 0.00% | 39.09 |
| reading_154 | noncoding | reading_cause | 7 | 0 | 0.00% | 41.66 |
| reading_155 | noncoding | reading_location | 7 | 0 | 0.00% | 39.77 |
| reading_159 | noncoding | reading_cause | 7 | 0 | 0.00% | 39.60 |
| reading_160 | noncoding | reading_location | 7 | 0 | 0.00% | 42.34 |
| reading_164 | noncoding | reading_cause | 7 | 0 | 0.00% | 39.94 |
| reading_165 | noncoding | reading_location | 7 | 0 | 0.00% | 39.43 |
| reading_169 | noncoding | reading_cause | 7 | 0 | 0.00% | 41.83 |
| reading_170 | noncoding | reading_location | 7 | 0 | 0.00% | 42.51 |
| reading_174 | noncoding | reading_cause | 7 | 0 | 0.00% | 40.46 |
| reading_175 | noncoding | reading_location | 7 | 0 | 0.00% | 38.74 |
| reading_179 | noncoding | reading_cause | 7 | 0 | 0.00% | 40.80 |
| reading_180 | noncoding | reading_location | 7 | 0 | 0.00% | 40.11 |
| reading_184 | noncoding | reading_cause | 7 | 0 | 0.00% | 39.94 |
| reading_185 | noncoding | reading_location | 7 | 0 | 0.00% | 41.49 |
| reading_189 | noncoding | reading_cause | 7 | 0 | 0.00% | 38.57 |
| reading_190 | noncoding | reading_location | 7 | 0 | 0.00% | 39.60 |
| reading_194 | noncoding | reading_cause | 7 | 0 | 0.00% | 39.26 |
| reading_195 | noncoding | reading_location | 7 | 0 | 0.00% | 39.94 |
| reading_199 | noncoding | reading_cause | 7 | 0 | 0.00% | 39.94 |
| reading_200 | noncoding | reading_location | 7 | 0 | 0.00% | 37.20 |
| reading_018 | noncoding | reading_quantity | 7 | 1 | 14.29% | 38.06 |
| reading_025 | noncoding | reading_location | 7 | 1 | 14.29% | 39.94 |
| reading_048 | noncoding | reading_quantity | 7 | 1 | 14.29% | 40.29 |
| reading_055 | noncoding | reading_location | 7 | 1 | 14.29% | 40.46 |
| reading_057 | noncoding | reading_date | 7 | 1 | 14.29% | 40.29 |
| reading_080 | noncoding | reading_location | 7 | 1 | 14.29% | 40.80 |
| reading_095 | noncoding | reading_location | 7 | 1 | 14.29% | 41.49 |
| reading_105 | noncoding | reading_location | 7 | 1 | 14.29% | 41.49 |
| reading_110 | noncoding | reading_location | 7 | 1 | 14.29% | 40.80 |
| reading_026 | noncoding | reading_fact | 7 | 2 | 28.57% | 39.26 |
| reading_013 | noncoding | reading_quantity | 7 | 3 | 42.86% | 38.40 |
| reading_033 | noncoding | reading_quantity | 7 | 3 | 42.86% | 39.94 |
| reading_038 | noncoding | reading_quantity | 7 | 3 | 42.86% | 38.57 |
| reading_088 | noncoding | reading_quantity | 7 | 3 | 42.86% | 40.63 |
| reading_113 | noncoding | reading_quantity | 7 | 3 | 42.86% | 40.11 |
| reading_116 | noncoding | reading_fact | 7 | 3 | 42.86% | 41.14 |
| reading_133 | noncoding | reading_quantity | 7 | 3 | 42.86% | 37.71 |
| reading_143 | noncoding | reading_quantity | 7 | 3 | 42.86% | 38.74 |
| reading_153 | noncoding | reading_quantity | 7 | 3 | 42.86% | 38.74 |
| reading_196 | noncoding | reading_fact | 7 | 3 | 42.86% | 39.94 |
| reading_198 | noncoding | reading_quantity | 7 | 3 | 42.86% | 39.26 |
| reading_001 | noncoding | reading_fact | 7 | 4 | 57.14% | 38.06 |
| reading_003 | noncoding | reading_quantity | 7 | 4 | 57.14% | 41.31 |
| reading_006 | noncoding | reading_fact | 7 | 4 | 57.14% | 41.31 |
| reading_012 | noncoding | reading_date | 7 | 4 | 57.14% | 40.11 |
| reading_023 | noncoding | reading_quantity | 7 | 4 | 57.14% | 41.49 |
| reading_031 | noncoding | reading_fact | 7 | 4 | 57.14% | 38.57 |
| reading_032 | noncoding | reading_date | 7 | 4 | 57.14% | 36.69 |
| reading_043 | noncoding | reading_quantity | 7 | 4 | 57.14% | 39.43 |
| reading_071 | noncoding | reading_fact | 7 | 4 | 57.14% | 41.31 |
| reading_072 | noncoding | reading_date | 7 | 4 | 57.14% | 38.91 |
| reading_078 | noncoding | reading_quantity | 7 | 4 | 57.14% | 40.29 |
| reading_081 | noncoding | reading_fact | 7 | 4 | 57.14% | 37.71 |
| reading_082 | noncoding | reading_date | 7 | 4 | 57.14% | 41.31 |
| reading_091 | noncoding | reading_fact | 7 | 4 | 57.14% | 41.31 |
| reading_093 | noncoding | reading_quantity | 7 | 4 | 57.14% | 40.97 |
| reading_098 | noncoding | reading_quantity | 7 | 4 | 57.14% | 37.03 |
| reading_108 | noncoding | reading_quantity | 7 | 4 | 57.14% | 41.31 |
| reading_128 | noncoding | reading_quantity | 7 | 4 | 57.14% | 38.74 |
| reading_138 | noncoding | reading_quantity | 7 | 4 | 57.14% | 41.31 |
| reading_148 | noncoding | reading_quantity | 7 | 4 | 57.14% | 40.11 |
| reading_151 | noncoding | reading_fact | 7 | 4 | 57.14% | 40.63 |
| reading_157 | noncoding | reading_date | 7 | 4 | 57.14% | 38.91 |
| reading_161 | noncoding | reading_fact | 7 | 4 | 57.14% | 40.80 |
| reading_166 | noncoding | reading_fact | 7 | 4 | 57.14% | 40.80 |
| reading_186 | noncoding | reading_fact | 7 | 4 | 57.14% | 41.31 |
| reading_021 | noncoding | reading_fact | 7 | 5 | 71.43% | 39.09 |
| reading_028 | noncoding | reading_quantity | 7 | 5 | 71.43% | 39.09 |
| reading_041 | noncoding | reading_fact | 7 | 5 | 71.43% | 37.54 |
| reading_046 | noncoding | reading_fact | 7 | 5 | 71.43% | 40.63 |
| reading_053 | noncoding | reading_quantity | 7 | 5 | 71.43% | 40.11 |
| reading_056 | noncoding | reading_fact | 7 | 5 | 71.43% | 41.49 |
| reading_058 | noncoding | reading_quantity | 7 | 5 | 71.43% | 39.43 |
| reading_063 | noncoding | reading_quantity | 7 | 5 | 71.43% | 37.54 |
| reading_067 | noncoding | reading_date | 7 | 5 | 71.43% | 35.83 |
| reading_068 | noncoding | reading_quantity | 7 | 5 | 71.43% | 41.31 |
| reading_076 | noncoding | reading_fact | 7 | 5 | 71.43% | 41.49 |
| reading_086 | noncoding | reading_fact | 7 | 5 | 71.43% | 39.60 |
| reading_096 | noncoding | reading_fact | 7 | 5 | 71.43% | 40.29 |
| reading_101 | noncoding | reading_fact | 7 | 5 | 71.43% | 42.00 |
| reading_103 | noncoding | reading_quantity | 7 | 5 | 71.43% | 41.49 |
| reading_111 | noncoding | reading_fact | 7 | 5 | 71.43% | 40.11 |
| reading_118 | noncoding | reading_quantity | 7 | 5 | 71.43% | 39.26 |
| reading_126 | noncoding | reading_fact | 7 | 5 | 71.43% | 42.51 |
| reading_136 | noncoding | reading_fact | 7 | 5 | 71.43% | 38.74 |
| reading_142 | noncoding | reading_date | 7 | 5 | 71.43% | 37.89 |
| reading_171 | noncoding | reading_fact | 7 | 5 | 71.43% | 38.57 |
| reading_172 | noncoding | reading_date | 7 | 5 | 71.43% | 38.91 |
| reading_181 | noncoding | reading_fact | 7 | 5 | 71.43% | 39.26 |
| reading_183 | noncoding | reading_quantity | 7 | 5 | 71.43% | 39.60 |
| reading_188 | noncoding | reading_quantity | 7 | 5 | 71.43% | 41.14 |
| reading_192 | noncoding | reading_date | 7 | 5 | 71.43% | 36.17 |
| reading_193 | noncoding | reading_quantity | 7 | 5 | 71.43% | 39.26 |
| reading_008 | noncoding | reading_quantity | 7 | 6 | 85.71% | 40.46 |
| reading_011 | noncoding | reading_fact | 7 | 6 | 85.71% | 39.94 |
| reading_016 | noncoding | reading_fact | 7 | 6 | 85.71% | 39.60 |
| reading_017 | noncoding | reading_date | 7 | 6 | 85.71% | 38.74 |
| reading_036 | noncoding | reading_fact | 7 | 6 | 85.71% | 41.66 |
| reading_037 | noncoding | reading_date | 7 | 6 | 85.71% | 40.63 |
| reading_042 | noncoding | reading_date | 7 | 6 | 85.71% | 41.66 |
| reading_047 | noncoding | reading_date | 7 | 6 | 85.71% | 40.11 |
| reading_051 | noncoding | reading_fact | 7 | 6 | 85.71% | 37.37 |
| reading_052 | noncoding | reading_date | 7 | 6 | 85.71% | 38.40 |
| reading_062 | noncoding | reading_date | 7 | 6 | 85.71% | 42.00 |
| reading_066 | noncoding | reading_fact | 7 | 6 | 85.71% | 39.43 |
| reading_073 | noncoding | reading_quantity | 7 | 6 | 85.71% | 40.80 |
| reading_077 | noncoding | reading_date | 7 | 6 | 85.71% | 41.31 |
| reading_083 | noncoding | reading_quantity | 7 | 6 | 85.71% | 41.49 |
| reading_092 | noncoding | reading_date | 7 | 6 | 85.71% | 38.74 |
| reading_102 | noncoding | reading_date | 7 | 6 | 85.71% | 39.94 |
| reading_106 | noncoding | reading_fact | 7 | 6 | 85.71% | 38.57 |
| reading_107 | noncoding | reading_date | 7 | 6 | 85.71% | 37.71 |
| reading_112 | noncoding | reading_date | 7 | 6 | 85.71% | 38.40 |
| reading_121 | noncoding | reading_fact | 7 | 6 | 85.71% | 41.31 |
| reading_127 | noncoding | reading_date | 7 | 6 | 85.71% | 40.29 |
| reading_131 | noncoding | reading_fact | 7 | 6 | 85.71% | 41.49 |
| reading_132 | noncoding | reading_date | 7 | 6 | 85.71% | 41.31 |
| reading_141 | noncoding | reading_fact | 7 | 6 | 85.71% | 40.29 |
| reading_146 | noncoding | reading_fact | 7 | 6 | 85.71% | 38.91 |
| reading_147 | noncoding | reading_date | 7 | 6 | 85.71% | 36.34 |
| reading_156 | noncoding | reading_fact | 7 | 6 | 85.71% | 39.09 |
| reading_158 | noncoding | reading_quantity | 7 | 6 | 85.71% | 39.09 |
| reading_162 | noncoding | reading_date | 7 | 6 | 85.71% | 38.57 |
| reading_163 | noncoding | reading_quantity | 7 | 6 | 85.71% | 39.94 |
| reading_167 | noncoding | reading_date | 7 | 6 | 85.71% | 38.06 |
| reading_168 | noncoding | reading_quantity | 7 | 6 | 85.71% | 41.31 |
| reading_173 | noncoding | reading_quantity | 7 | 6 | 85.71% | 41.31 |
| reading_177 | noncoding | reading_date | 7 | 6 | 85.71% | 39.94 |
| reading_178 | noncoding | reading_quantity | 7 | 6 | 85.71% | 38.06 |
| reading_187 | noncoding | reading_date | 7 | 6 | 85.71% | 38.57 |
| reading_191 | noncoding | reading_fact | 7 | 6 | 85.71% | 40.63 |
| reading_002 | noncoding | reading_date | 7 | 7 | 100.00% | 39.26 |
| reading_007 | noncoding | reading_date | 7 | 7 | 100.00% | 39.43 |
| reading_022 | noncoding | reading_date | 7 | 7 | 100.00% | 39.26 |
| reading_027 | noncoding | reading_date | 7 | 7 | 100.00% | 36.69 |
| reading_061 | noncoding | reading_fact | 7 | 7 | 100.00% | 39.60 |
| reading_087 | noncoding | reading_date | 7 | 7 | 100.00% | 37.54 |
| reading_097 | noncoding | reading_date | 7 | 7 | 100.00% | 40.63 |
| reading_117 | noncoding | reading_date | 7 | 7 | 100.00% | 35.83 |
| reading_122 | noncoding | reading_date | 7 | 7 | 100.00% | 38.74 |
| reading_123 | noncoding | reading_quantity | 7 | 7 | 100.00% | 38.23 |
| reading_137 | noncoding | reading_date | 7 | 7 | 100.00% | 38.57 |
| reading_152 | noncoding | reading_date | 7 | 7 | 100.00% | 39.60 |
| reading_176 | noncoding | reading_fact | 7 | 7 | 100.00% | 39.43 |
| reading_182 | noncoding | reading_date | 7 | 7 | 100.00% | 38.91 |
| reading_197 | noncoding | reading_date | 7 | 7 | 100.00% | 38.40 |

## Model failures

There were **788** valid model responses that did not pass their deterministic scorer. The first 100 are listed below.

| Task | Font | Size px | Patches | Response |
|---|---|---|---|---|
| reading_004 | fira-sans | 8 | 36 | Because the inventory count took longer than expected. |
| reading_005 | fira-sans | 8 | 35 | The field station |
| reading_008 | fira-sans | 8 | 35 | 40 cases |
| reading_009 | fira-sans | 8 | 36 | Because the calibration check had to be repeated. |
| reading_010 | fira-sans | 8 | 35 | The upper archive |
| reading_014 | fira-sans | 8 | 35 | Because he was dealing with a delayed delivery. |
| reading_015 | fira-sans | 8 | 36 | The west depot |
| reading_018 | fira-sans | 8 | 35 | 35 |
| reading_019 | fira-sans | 8 | 39 | Because the window was extended. |
| reading_020 | fira-sans | 8 | 35 | The upper archive. |
| reading_024 | fira-sans | 8 | 35 | Because the temperature sensor failed. |
| reading_025 | fira-sans | 8 | 35 | The west depot |
| reading_026 | fira-sans | 8 | 35 | Felix and Raa? |
| reading_029 | fira-sans | 8 | 39 | Because the replacement key had not arrived. |
| reading_030 | fira-sans | 8 | 36 | technical office |
| reading_033 | fira-sans | 8 | 35 | 72 cases |
| reading_034 | fira-sans | 8 | 35 | The delivery truck arrived late. |
| reading_035 | fira-sans | 8 | 35 | Temporary staging areas mentioned in older notes |
| reading_036 | fira-sans | 8 | 36 | harbor |
| reading_039 | fira-sans | 8 | 35 | The replacement key had not arrived. |
| reading_040 | fira-sans | 8 | 35 | The training room |
| reading_044 | fira-sans | 8 | 35 | Because the temperature sensor failed. |
| reading_045 | fira-sans | 8 | 35 | the south workshop |
| reading_048 | fira-sans | 8 | 35 | 5 crates |
| reading_049 | fira-sans | 8 | 35 | Because he had been delayed on the outdoor work. |
| reading_050 | fira-sans | 8 | 35 | The east annex |
| reading_054 | fira-sans | 8 | 35 | Because the calibration check had to be repeated. |
| reading_055 | fira-sans | 8 | 35 | the central office |
| reading_057 | fira-sans | 8 | 35 | February 19th |
| reading_059 | fira-sans | 8 | 35 | Because the inventory count took longer than expected. |
| reading_060 | fira-sans | 8 | 39 | The east annex |
| reading_064 | fira-sans | 8 | 36 | He was worried about taking longer than expected. |
| reading_065 | fira-sans | 8 | 36 | In the staging areas mentioned in older notes. |
| reading_069 | fira-sans | 8 | 36 | The calibration check had to be repeated. |
| reading_070 | fira-sans | 8 | 36 | The training room |
| reading_074 | fira-sans | 8 | 36 | Because the inventory count took longer than expected. |
| reading_075 | fira-sans | 8 | 35 | the upper archive |
| reading_078 | fira-sans | 8 | 35 | 6 |
| reading_079 | fira-sans | 8 | 35 | Because the inventory count took longer than expected. |
| reading_080 | fira-sans | 8 | 36 | The dispatch bay. |
| reading_082 | fira-sans | 8 | 36 | Friday |
| reading_084 | fira-sans | 8 | 33 | A special approval was needed. |
| reading_085 | fira-sans | 8 | 35 | the west depot |
| reading_089 | fira-sans | 8 | 35 | The replacement key had not arrived. |
| reading_090 | fira-sans | 8 | 39 | The north warehouse. |
| reading_094 | fira-sans | 8 | 39 | The network maintenance window was extended. |
| reading_098 | fira-sans | 8 | 32 | 86 kits |
| reading_099 | fira-sans | 8 | 35 | Because a supplier changed the pickup time. |
| reading_100 | fira-sans | 8 | 35 | The field station |
| reading_104 | fira-sans | 8 | 35 | Because the F? was delayed. |
| reading_108 | fira-sans | 8 | 36 | 74 samples |
| reading_109 | fira-sans | 8 | 35 | Because the network maintenance window was extended. |
| reading_110 | fira-sans | 8 | 35 | The upper archive |
| reading_113 | fira-sans | 8 | 36 | 5 modules |
| reading_114 | fira-sans | 8 | 35 | Because the calibration check had to be repeated. |
| reading_115 | fira-sans | 8 | 35 | In the field station. |
| reading_118 | fira-sans | 8 | 35 | Four |
| reading_119 | fira-sans | 8 | 35 | Because the inventory count took longer than expected. |
| reading_120 | fira-sans | 8 | 36 | The upper archive. |
| reading_124 | fira-sans | 8 | 39 | Heavy rain delayed the outdoor work. |
| reading_125 | fira-sans | 8 | 36 | The upper archive |
| reading_129 | fira-sans | 8 | 35 | Because a supplier changed the pickup time. |
| reading_130 | fira-sans | 8 | 35 | In the river lab. |
| reading_134 | fira-sans | 8 | 35 | Because the delivery truck arrived late. |
| reading_135 | fira-sans | 8 | 40 | The west depot |
| reading_139 | fira-sans | 8 | 35 | Because the calibration check had to be repeated. |
| reading_140 | fira-sans | 8 | 35 | The west depot |
| reading_144 | fira-sans | 8 | 39 | The calibration check had to be repeated. |
| reading_145 | fira-sans | 8 | 35 | the east annex |
| reading_149 | fira-sans | 8 | 39 | Because the calibration check had to be repeated. |
| reading_150 | fira-sans | 8 | 35 | the river lab |
| reading_154 | fira-sans | 8 | 36 | The calibration check had to be repeated. |
| reading_155 | fira-sans | 8 | 35 | The south workshop |
| reading_159 | fira-sans | 8 | 35 | Because a safety drill required the main hall. |
| reading_160 | fira-sans | 8 | 36 | The field station. |
| reading_164 | fira-sans | 8 | 35 | A safety drill occurred that afternoon. |
| reading_165 | fira-sans | 8 | 35 | The training room |
| reading_169 | fira-sans | 8 | 36 | Because the delivery truck arrived late. |
| reading_170 | fira-sans | 8 | 39 | The west depot |
| reading_174 | fira-sans | 8 | 35 | Because the network maintenance window was extended. |
| reading_175 | fira-sans | 8 | 35 | The eastern staging area. |
| reading_177 | fira-sans | 8 | 35 | The date is not specified. |
| reading_179 | fira-sans | 8 | 36 | Heavy rain delayed the outdoor work. |
| reading_180 | fira-sans | 8 | 35 | In the central office |
| reading_184 | fira-sans | 8 | 35 | The delivery truck arrived late. |
| reading_185 | fira-sans | 8 | 36 | The upper archive. |
| reading_188 | fira-sans | 8 | 35 | 9 sensors |
| reading_189 | fira-sans | 8 | 35 | Because a safety drill occurred in the main hall. |
| reading_190 | fira-sans | 8 | 35 | The dispatch bay. |
| reading_194 | fira-sans | 8 | 35 | The temperature sensor failed. |
| reading_195 | fira-sans | 8 | 35 | The river lab |
| reading_196 | fira-sans | 8 | 35 | work |
| reading_199 | fira-sans | 8 | 35 | Because the network maintenance window was extended. |
| reading_200 | fira-sans | 8 | 32 | The central office. |
| reading_003 | atkinson-hyperlegible | 8 | 27 | 76 samples |
| reading_004 | atkinson-hyperlegible | 8 | 27 | He noticed a discrepancy in the records that needed to be verified first. |
| reading_005 | atkinson-hyperlegible | 8 | 25 | The river lab. |
| reading_009 | atkinson-hyperlegible | 8 | 27 | Because the checklist had to be repeated. |
| reading_010 | atkinson-hyperlegible | 8 | 24 | The upper archive |
| reading_012 | atkinson-hyperlegible | 8 | 25 | April 5 |

## Infrastructure failures

No infrastructure failures were observed.

## Interpretation notes

- `estimated_image_tokens` uses the configured 1.2-token-per-32×32-patch estimate recorded by the renderer; it is an estimate, not a replacement for any usage fields reported by Codex/OpenAI.
- The Pareto frontier is descriptive for this exact task corpus and run. It treats higher accuracy and lower mean estimated image tokens as better; it is not a statistical equivalence test.
- Coding and non-coding results are shown separately because character-level damage can affect source-code-like instructions differently from redundant natural language.
- Infrastructure failures are excluded from accuracy denominators and retained separately in the raw results.
- `results.csv` is the flattened row-per-image analysis dataset. `results.jsonl` preserves substantially richer Codex event and scoring evidence.

## Category × font

The compact cells below are passed/valid (accuracy); every cell has n=40. The detailed table includes Wilson intervals and token estimates.

| Category | atkinson-hyperlegible | fira-sans | ibm-plex-sans | inter | jetbrains-mono | noto-sans | source-sans-3 |
|---|---|---|---|---|---|---|---|
| reading_cause | 0/40 (0.00%) | 0/40 (0.00%) | 0/40 (0.00%) | 0/40 (0.00%) | 0/40 (0.00%) | 0/40 (0.00%) | 0/40 (0.00%) |
| reading_date | 28/40 (70.00%) | 37/40 (92.50%) | 32/40 (80.00%) | 37/40 (92.50%) | 36/40 (90.00%) | 27/40 (67.50%) | 36/40 (90.00%) |
| reading_fact | 21/40 (52.50%) | 37/40 (92.50%) | 25/40 (62.50%) | 35/40 (87.50%) | 35/40 (87.50%) | 20/40 (50.00%) | 26/40 (65.00%) |
| reading_location | 1/40 (2.50%) | 2/40 (5.00%) | 0/40 (0.00%) | 1/40 (2.50%) | 0/40 (0.00%) | 1/40 (2.50%) | 1/40 (2.50%) |
| reading_quantity | 17/40 (42.50%) | 30/40 (75.00%) | 18/40 (45.00%) | 30/40 (75.00%) | 37/40 (92.50%) | 22/40 (55.00%) | 20/40 (50.00%) |

| Category | Font | Passed/valid | Accuracy | Wilson 95% CI | Mean patches | Mean est. image tokens |
|---|---|---|---|---|---|---|
| reading_cause | atkinson-hyperlegible | 0/40 | 0.00% | 0.00%–8.76% | 25.93 | 31.11 |
| reading_cause | fira-sans | 0/40 | 0.00% | 0.00%–8.76% | 35.75 | 42.90 |
| reading_cause | ibm-plex-sans | 0/40 | 0.00% | 0.00%–8.76% | 30.75 | 36.90 |
| reading_cause | inter | 0/40 | 0.00% | 0.00%–8.76% | 39.83 | 47.79 |
| reading_cause | jetbrains-mono | 0/40 | 0.00% | 0.00%–8.76% | 46.15 | 55.38 |
| reading_cause | noto-sans | 0/40 | 0.00% | 0.00%–8.76% | 32.50 | 39.00 |
| reading_cause | source-sans-3 | 0/40 | 0.00% | 0.00%–8.76% | 25.65 | 30.78 |
| reading_date | atkinson-hyperlegible | 28/40 | 70.00% | 54.57%–81.93% | 25.00 | 30.00 |
| reading_date | fira-sans | 37/40 | 92.50% | 80.14%–97.42% | 34.67 | 41.61 |
| reading_date | ibm-plex-sans | 32/40 | 80.00% | 65.24%–89.50% | 29.52 | 35.43 |
| reading_date | inter | 37/40 | 92.50% | 80.14%–97.42% | 38.05 | 45.66 |
| reading_date | jetbrains-mono | 36/40 | 90.00% | 76.95%–96.04% | 44.33 | 53.19 |
| reading_date | noto-sans | 27/40 | 67.50% | 52.02%–79.92% | 31.07 | 37.29 |
| reading_date | source-sans-3 | 36/40 | 90.00% | 76.95%–96.04% | 24.65 | 29.58 |
| reading_fact | atkinson-hyperlegible | 21/40 | 52.50% | 37.50%–67.06% | 25.70 | 30.84 |
| reading_fact | fira-sans | 37/40 | 92.50% | 80.14%–97.42% | 35.27 | 42.33 |
| reading_fact | ibm-plex-sans | 25/40 | 62.50% | 47.03%–75.78% | 30.38 | 36.45 |
| reading_fact | inter | 35/40 | 87.50% | 73.89%–94.54% | 39.25 | 47.10 |
| reading_fact | jetbrains-mono | 35/40 | 87.50% | 73.89%–94.54% | 45.55 | 54.66 |
| reading_fact | noto-sans | 20/40 | 50.00% | 35.20%–64.80% | 32.05 | 38.46 |
| reading_fact | source-sans-3 | 26/40 | 65.00% | 49.51%–77.87% | 25.25 | 30.30 |
| reading_location | atkinson-hyperlegible | 1/40 | 2.50% | 0.44%–12.88% | 25.93 | 31.11 |
| reading_location | fira-sans | 2/40 | 5.00% | 1.38%–16.50% | 35.62 | 42.75 |
| reading_location | ibm-plex-sans | 0/40 | 0.00% | 0.00%–8.76% | 30.73 | 36.87 |
| reading_location | inter | 1/40 | 2.50% | 0.44%–12.88% | 39.65 | 47.58 |
| reading_location | jetbrains-mono | 0/40 | 0.00% | 0.00%–8.76% | 45.90 | 55.08 |
| reading_location | noto-sans | 1/40 | 2.50% | 0.44%–12.88% | 32.38 | 38.85 |
| reading_location | source-sans-3 | 1/40 | 2.50% | 0.44%–12.88% | 25.55 | 30.66 |
| reading_quantity | atkinson-hyperlegible | 17/40 | 42.50% | 28.51%–57.80% | 25.50 | 30.60 |
| reading_quantity | fira-sans | 30/40 | 75.00% | 59.81%–85.81% | 35.20 | 42.24 |
| reading_quantity | ibm-plex-sans | 18/40 | 45.00% | 30.71%–60.17% | 30.23 | 36.27 |
| reading_quantity | inter | 30/40 | 75.00% | 59.81%–85.81% | 38.95 | 46.74 |
| reading_quantity | jetbrains-mono | 37/40 | 92.50% | 80.14%–97.42% | 45.23 | 54.27 |
| reading_quantity | noto-sans | 22/40 | 55.00% | 39.83%–69.29% | 31.82 | 38.19 |
| reading_quantity | source-sans-3 | 20/40 | 50.00% | 35.20%–64.80% | 25.15 | 30.18 |

## JetBrains Mono control comparison

The paired comparison uses the same 200 task IDs and reports candidate minus control pass indicators. It is descriptive and is not a text baseline.

| Font | Candidate accuracy | Control accuracy | Paired better | Paired worse | Ties | Mean paired Δ |
|---|---:|---:|---:|---:|---:|---:|
| atkinson-hyperlegible | 33.50% | 54.00% | 6 | 47 | 147 | -0.205 |
| fira-sans | 53.00% | 54.00% | 10 | 12 | 178 | -0.010 |
| ibm-plex-sans | 37.50% | 54.00% | 8 | 41 | 151 | -0.165 |
| inter | 51.50% | 54.00% | 10 | 15 | 175 | -0.025 |
| noto-sans | 35.00% | 54.00% | 8 | 46 | 146 | -0.190 |
| source-sans-3 | 41.50% | 54.00% | 9 | 34 | 157 | -0.125 |

## Retry and failure accounting

- Final valid model observations: **1400** (612 pass, 788 deterministic scorer failures).
- Final infrastructure failures: **0**.
- Two observations had one infrastructure retry before final completion: `reading_012`/`ibm-plex-sans` and `reading_151`/`ibm-plex-sans`. Each final row has `attempts=2` and a valid scored response.
- Valid model failures were not retried. The two retries were infrastructure-triggered only.

## Task robustness summary

| Passes across 7 fonts | Tasks |
|---:|---:|
| 0/7 | 74 |
| 1/7 | 9 |
| 2/7 | 1 |
| 3/7 | 11 |
| 4/7 | 25 |
| 5/7 | 27 |
| 6/7 | 38 |
| 7/7 | 15 |
