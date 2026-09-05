# Reading-200 paired text/image benchmark report

Generated: `2026-09-05T16:57:15.021089+00:00`  
Run ID: `reading-200-paired-20260905T162830Z-1f1a0343`  
Model: `gpt-5.6-luna`  
Codex CLI: `codex-cli 0.153.4`  
Dataset SHA-256: `987988ff39e3ed843ec1b6bb0b6287415c4cbfea83edf6ca4c60a7a25b6f1aef`  
Image manifest SHA-256: `60e10f54d4634514662be6b32f80c04d7f18e43fa535e3dee9cbe4e82e893a3e`

The dataset and PNG corpus are immutable committed inputs. Every observation used a fresh `codex exec --ephemeral` child session. Image observations supplied the passage only through the assigned PNG; text observations supplied the original passage as text. No text/image equivalence claim is made beyond these paired results.

## Completion and isolation

- Total observations: **1200** (1000 image + 200 text)
- Valid scored observations: **1200**
- Final infrastructure failures: **0**
- Rows with infrastructure retries: **0**
- Unique child thread IDs: **1200**

## Plain-text baseline

- Accuracy: **125/200 = 62.50%** (Wilson 95% CI 55.61%–68.91%)
- Mean latency: **4992 ms**
- Observed Codex input tokens: **13302.80 mean** (13006–14339, n=200)

## Image results by size

| Size | Passed/valid | Accuracy | Wilson 95% CI | Gap vs text | Mean patches | Mean est. image tokens | Mean latency ms |
|---|---|---|---|---|---|---|---|
| 8px | 102/200 | 51.00% | 44.12%–57.84% | -11.50% | 35.30 | 42.37 | 7909 |
| 9px | 110/200 | 55.00% | 48.08%–61.74% | -7.50% | 39.72 | 47.66 | 6465 |
| 10px | 114/200 | 57.00% | 50.07%–63.67% | -5.50% | 50.73 | 60.87 | 5275 |
| 11px | 104/200 | 52.00% | 45.10%–58.82% | -10.50% | 55.67 | 66.80 | 5112 |
| 12px | 104/200 | 52.00% | 45.10%–58.82% | -10.50% | 68.81 | 82.58 | 4700 |

Smallest size closest to text-baseline accuracy: **10px** (absolute gap 5.50%).

## Category accuracy

Text baseline:

| Category | Passed/valid | Accuracy | Wilson 95% CI |
|---|---|---|---|
| reading_cause | 0/40 | 0.00% | 0.00%–8.76% |
| reading_date | 40/40 | 100.00% | 91.24%–100.00% |
| reading_fact | 40/40 | 100.00% | 91.24%–100.00% |
| reading_location | 5/40 | 12.50% | 5.46%–26.11% |
| reading_quantity | 40/40 | 100.00% | 91.24%–100.00% |

Image conditions:

| Size | Category | Passed/valid | Accuracy | Wilson 95% CI |
|---|---|---|---|---|
| 8px | reading_cause | 0/40 | 0.00% | 0.00%–8.76% |
| 9px | reading_cause | 0/40 | 0.00% | 0.00%–8.76% |
| 10px | reading_cause | 0/40 | 0.00% | 0.00%–8.76% |
| 11px | reading_cause | 0/40 | 0.00% | 0.00%–8.76% |
| 12px | reading_cause | 0/40 | 0.00% | 0.00%–8.76% |
| 8px | reading_date | 38/40 | 95.00% | 83.50%–98.62% |
| 9px | reading_date | 39/40 | 97.50% | 87.12%–99.56% |
| 10px | reading_date | 40/40 | 100.00% | 91.24%–100.00% |
| 11px | reading_date | 37/40 | 92.50% | 80.14%–97.42% |
| 12px | reading_date | 32/40 | 80.00% | 65.24%–89.50% |
| 8px | reading_fact | 35/40 | 87.50% | 73.89%–94.54% |
| 9px | reading_fact | 36/40 | 90.00% | 76.95%–96.04% |
| 10px | reading_fact | 37/40 | 92.50% | 80.14%–97.42% |
| 11px | reading_fact | 30/40 | 75.00% | 59.81%–85.81% |
| 12px | reading_fact | 35/40 | 87.50% | 73.89%–94.54% |
| 8px | reading_location | 2/40 | 5.00% | 1.38%–16.50% |
| 9px | reading_location | 1/40 | 2.50% | 0.44%–12.88% |
| 10px | reading_location | 1/40 | 2.50% | 0.44%–12.88% |
| 11px | reading_location | 2/40 | 5.00% | 1.38%–16.50% |
| 12px | reading_location | 2/40 | 5.00% | 1.38%–16.50% |
| 8px | reading_quantity | 27/40 | 67.50% | 52.02%–79.92% |
| 9px | reading_quantity | 34/40 | 85.00% | 70.93%–92.94% |
| 10px | reading_quantity | 36/40 | 90.00% | 76.95%–96.04% |
| 11px | reading_quantity | 35/40 | 87.50% | 73.89%–94.54% |
| 12px | reading_quantity | 35/40 | 87.50% | 73.89%–94.54% |

Cause/location recovery from 8px to 12px:

| Category | 8px | 12px | Change |
|---|---|---|---|
| reading_cause | 0.00% | 0.00% | +0.00% |
| reading_location | 5.00% | 5.00% | +0.00% |

## Task-by-task recovery from 8px to 12px

Recovered (8px fail → 12px pass): **19**; regressed: **17**; stable pass: **85**; stable fail: **79**.

| Task | Category | 8px | 12px | Delta |
|---|---|---|---|---|
| reading_001 | reading_fact | PASS | PASS | +0 |
| reading_002 | reading_date | PASS | PASS | +0 |
| reading_003 | reading_quantity | PASS | FAIL | -1 |
| reading_004 | reading_cause | FAIL | FAIL | +0 |
| reading_005 | reading_location | FAIL | FAIL | +0 |
| reading_006 | reading_fact | PASS | PASS | +0 |
| reading_007 | reading_date | PASS | PASS | +0 |
| reading_008 | reading_quantity | PASS | PASS | +0 |
| reading_009 | reading_cause | FAIL | FAIL | +0 |
| reading_010 | reading_location | FAIL | FAIL | +0 |
| reading_011 | reading_fact | PASS | PASS | +0 |
| reading_012 | reading_date | PASS | PASS | +0 |
| reading_013 | reading_quantity | PASS | PASS | +0 |
| reading_014 | reading_cause | FAIL | FAIL | +0 |
| reading_015 | reading_location | FAIL | FAIL | +0 |
| reading_016 | reading_fact | PASS | FAIL | -1 |
| reading_017 | reading_date | PASS | PASS | +0 |
| reading_018 | reading_quantity | PASS | PASS | +0 |
| reading_019 | reading_cause | FAIL | FAIL | +0 |
| reading_020 | reading_location | FAIL | FAIL | +0 |
| reading_021 | reading_fact | PASS | PASS | +0 |
| reading_022 | reading_date | PASS | FAIL | -1 |
| reading_023 | reading_quantity | PASS | PASS | +0 |
| reading_024 | reading_cause | FAIL | FAIL | +0 |
| reading_025 | reading_location | FAIL | FAIL | +0 |
| reading_026 | reading_fact | PASS | PASS | +0 |
| reading_027 | reading_date | PASS | PASS | +0 |
| reading_028 | reading_quantity | FAIL | PASS | +1 |
| reading_029 | reading_cause | FAIL | FAIL | +0 |
| reading_030 | reading_location | FAIL | FAIL | +0 |
| reading_031 | reading_fact | PASS | PASS | +0 |
| reading_032 | reading_date | PASS | PASS | +0 |
| reading_033 | reading_quantity | FAIL | PASS | +1 |
| reading_034 | reading_cause | FAIL | FAIL | +0 |
| reading_035 | reading_location | FAIL | FAIL | +0 |
| reading_036 | reading_fact | FAIL | PASS | +1 |
| reading_037 | reading_date | PASS | FAIL | -1 |
| reading_038 | reading_quantity | PASS | PASS | +0 |
| reading_039 | reading_cause | FAIL | FAIL | +0 |
| reading_040 | reading_location | FAIL | FAIL | +0 |
| reading_041 | reading_fact | PASS | PASS | +0 |
| reading_042 | reading_date | PASS | FAIL | -1 |
| reading_043 | reading_quantity | PASS | PASS | +0 |
| reading_044 | reading_cause | FAIL | FAIL | +0 |
| reading_045 | reading_location | FAIL | FAIL | +0 |
| reading_046 | reading_fact | PASS | PASS | +0 |
| reading_047 | reading_date | PASS | PASS | +0 |
| reading_048 | reading_quantity | FAIL | PASS | +1 |
| reading_049 | reading_cause | FAIL | FAIL | +0 |
| reading_050 | reading_location | FAIL | FAIL | +0 |
| reading_051 | reading_fact | PASS | PASS | +0 |
| reading_052 | reading_date | PASS | PASS | +0 |
| reading_053 | reading_quantity | FAIL | PASS | +1 |
| reading_054 | reading_cause | FAIL | FAIL | +0 |
| reading_055 | reading_location | FAIL | FAIL | +0 |
| reading_056 | reading_fact | PASS | FAIL | -1 |
| reading_057 | reading_date | PASS | PASS | +0 |
| reading_058 | reading_quantity | PASS | PASS | +0 |
| reading_059 | reading_cause | FAIL | FAIL | +0 |
| reading_060 | reading_location | FAIL | FAIL | +0 |
| reading_061 | reading_fact | PASS | PASS | +0 |
| reading_062 | reading_date | FAIL | PASS | +1 |
| reading_063 | reading_quantity | PASS | PASS | +0 |
| reading_064 | reading_cause | FAIL | FAIL | +0 |
| reading_065 | reading_location | FAIL | FAIL | +0 |
| reading_066 | reading_fact | PASS | PASS | +0 |
| reading_067 | reading_date | PASS | PASS | +0 |
| reading_068 | reading_quantity | PASS | PASS | +0 |
| reading_069 | reading_cause | FAIL | FAIL | +0 |
| reading_070 | reading_location | FAIL | FAIL | +0 |
| reading_071 | reading_fact | FAIL | PASS | +1 |
| reading_072 | reading_date | PASS | PASS | +0 |
| reading_073 | reading_quantity | PASS | PASS | +0 |
| reading_074 | reading_cause | FAIL | FAIL | +0 |
| reading_075 | reading_location | FAIL | FAIL | +0 |
| reading_076 | reading_fact | PASS | PASS | +0 |
| reading_077 | reading_date | PASS | PASS | +0 |
| reading_078 | reading_quantity | FAIL | PASS | +1 |
| reading_079 | reading_cause | FAIL | FAIL | +0 |
| reading_080 | reading_location | PASS | PASS | +0 |
| reading_081 | reading_fact | PASS | PASS | +0 |
| reading_082 | reading_date | PASS | PASS | +0 |
| reading_083 | reading_quantity | PASS | PASS | +0 |
| reading_084 | reading_cause | FAIL | FAIL | +0 |
| reading_085 | reading_location | FAIL | FAIL | +0 |
| reading_086 | reading_fact | PASS | PASS | +0 |
| reading_087 | reading_date | PASS | PASS | +0 |
| reading_088 | reading_quantity | PASS | PASS | +0 |
| reading_089 | reading_cause | FAIL | FAIL | +0 |
| reading_090 | reading_location | FAIL | FAIL | +0 |
| reading_091 | reading_fact | PASS | PASS | +0 |
| reading_092 | reading_date | PASS | PASS | +0 |
| reading_093 | reading_quantity | PASS | PASS | +0 |
| reading_094 | reading_cause | FAIL | FAIL | +0 |
| reading_095 | reading_location | FAIL | FAIL | +0 |
| reading_096 | reading_fact | PASS | PASS | +0 |
| reading_097 | reading_date | PASS | PASS | +0 |
| reading_098 | reading_quantity | FAIL | PASS | +1 |
| reading_099 | reading_cause | FAIL | FAIL | +0 |
| reading_100 | reading_location | FAIL | FAIL | +0 |
| reading_101 | reading_fact | PASS | FAIL | -1 |
| reading_102 | reading_date | PASS | PASS | +0 |
| reading_103 | reading_quantity | PASS | PASS | +0 |
| reading_104 | reading_cause | FAIL | FAIL | +0 |
| reading_105 | reading_location | FAIL | FAIL | +0 |
| reading_106 | reading_fact | PASS | PASS | +0 |
| reading_107 | reading_date | PASS | PASS | +0 |
| reading_108 | reading_quantity | PASS | PASS | +0 |
| reading_109 | reading_cause | FAIL | FAIL | +0 |
| reading_110 | reading_location | PASS | FAIL | -1 |
| reading_111 | reading_fact | PASS | PASS | +0 |
| reading_112 | reading_date | PASS | PASS | +0 |
| reading_113 | reading_quantity | FAIL | FAIL | +0 |
| reading_114 | reading_cause | FAIL | FAIL | +0 |
| reading_115 | reading_location | FAIL | FAIL | +0 |
| reading_116 | reading_fact | PASS | PASS | +0 |
| reading_117 | reading_date | PASS | PASS | +0 |
| reading_118 | reading_quantity | FAIL | PASS | +1 |
| reading_119 | reading_cause | FAIL | FAIL | +0 |
| reading_120 | reading_location | FAIL | FAIL | +0 |
| reading_121 | reading_fact | FAIL | PASS | +1 |
| reading_122 | reading_date | PASS | PASS | +0 |
| reading_123 | reading_quantity | FAIL | PASS | +1 |
| reading_124 | reading_cause | FAIL | FAIL | +0 |
| reading_125 | reading_location | FAIL | FAIL | +0 |
| reading_126 | reading_fact | FAIL | PASS | +1 |
| reading_127 | reading_date | PASS | FAIL | -1 |
| reading_128 | reading_quantity | FAIL | FAIL | +0 |
| reading_129 | reading_cause | FAIL | FAIL | +0 |
| reading_130 | reading_location | FAIL | FAIL | +0 |
| reading_131 | reading_fact | PASS | FAIL | -1 |
| reading_132 | reading_date | PASS | PASS | +0 |
| reading_133 | reading_quantity | PASS | FAIL | -1 |
| reading_134 | reading_cause | FAIL | FAIL | +0 |
| reading_135 | reading_location | FAIL | FAIL | +0 |
| reading_136 | reading_fact | PASS | PASS | +0 |
| reading_137 | reading_date | FAIL | PASS | +1 |
| reading_138 | reading_quantity | FAIL | PASS | +1 |
| reading_139 | reading_cause | FAIL | FAIL | +0 |
| reading_140 | reading_location | FAIL | FAIL | +0 |
| reading_141 | reading_fact | PASS | PASS | +0 |
| reading_142 | reading_date | PASS | FAIL | -1 |
| reading_143 | reading_quantity | PASS | PASS | +0 |
| reading_144 | reading_cause | FAIL | FAIL | +0 |
| reading_145 | reading_location | FAIL | FAIL | +0 |
| reading_146 | reading_fact | PASS | PASS | +0 |
| reading_147 | reading_date | PASS | PASS | +0 |
| reading_148 | reading_quantity | PASS | PASS | +0 |
| reading_149 | reading_cause | FAIL | FAIL | +0 |
| reading_150 | reading_location | FAIL | FAIL | +0 |
| reading_151 | reading_fact | PASS | PASS | +0 |
| reading_152 | reading_date | PASS | PASS | +0 |
| reading_153 | reading_quantity | PASS | PASS | +0 |
| reading_154 | reading_cause | FAIL | FAIL | +0 |
| reading_155 | reading_location | FAIL | FAIL | +0 |
| reading_156 | reading_fact | PASS | FAIL | -1 |
| reading_157 | reading_date | PASS | FAIL | -1 |
| reading_158 | reading_quantity | PASS | PASS | +0 |
| reading_159 | reading_cause | FAIL | FAIL | +0 |
| reading_160 | reading_location | FAIL | FAIL | +0 |
| reading_161 | reading_fact | PASS | PASS | +0 |
| reading_162 | reading_date | PASS | PASS | +0 |
| reading_163 | reading_quantity | PASS | PASS | +0 |
| reading_164 | reading_cause | FAIL | FAIL | +0 |
| reading_165 | reading_location | FAIL | FAIL | +0 |
| reading_166 | reading_fact | PASS | PASS | +0 |
| reading_167 | reading_date | PASS | PASS | +0 |
| reading_168 | reading_quantity | FAIL | PASS | +1 |
| reading_169 | reading_cause | FAIL | FAIL | +0 |
| reading_170 | reading_location | FAIL | FAIL | +0 |
| reading_171 | reading_fact | PASS | PASS | +0 |
| reading_172 | reading_date | PASS | FAIL | -1 |
| reading_173 | reading_quantity | PASS | PASS | +0 |
| reading_174 | reading_cause | FAIL | FAIL | +0 |
| reading_175 | reading_location | FAIL | PASS | +1 |
| reading_176 | reading_fact | PASS | PASS | +0 |
| reading_177 | reading_date | PASS | PASS | +0 |
| reading_178 | reading_quantity | PASS | FAIL | -1 |
| reading_179 | reading_cause | FAIL | FAIL | +0 |
| reading_180 | reading_location | FAIL | FAIL | +0 |
| reading_181 | reading_fact | PASS | PASS | +0 |
| reading_182 | reading_date | PASS | FAIL | -1 |
| reading_183 | reading_quantity | FAIL | PASS | +1 |
| reading_184 | reading_cause | FAIL | FAIL | +0 |
| reading_185 | reading_location | FAIL | FAIL | +0 |
| reading_186 | reading_fact | PASS | PASS | +0 |
| reading_187 | reading_date | PASS | PASS | +0 |
| reading_188 | reading_quantity | PASS | PASS | +0 |
| reading_189 | reading_cause | FAIL | FAIL | +0 |
| reading_190 | reading_location | FAIL | FAIL | +0 |
| reading_191 | reading_fact | PASS | PASS | +0 |
| reading_192 | reading_date | PASS | PASS | +0 |
| reading_193 | reading_quantity | PASS | PASS | +0 |
| reading_194 | reading_cause | FAIL | FAIL | +0 |
| reading_195 | reading_location | FAIL | FAIL | +0 |
| reading_196 | reading_fact | FAIL | PASS | +1 |
| reading_197 | reading_date | PASS | PASS | +0 |
| reading_198 | reading_quantity | PASS | PASS | +0 |
| reading_199 | reading_cause | FAIL | FAIL | +0 |
| reading_200 | reading_location | FAIL | FAIL | +0 |

## Accuracy-vs-image-token Pareto frontier

| Size | Accuracy | Mean est. image tokens | Mean patches |
|---|---|---|---|
| 8px | 51.00% | 42.37 | 35.30 |
| 9px | 55.00% | 47.66 | 39.72 |
| 10px | 57.00% | 60.87 | 50.73 |

## Infrastructure failures and retries

No final infrastructure failures were observed.
