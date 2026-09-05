# Research Log

This file is the contemporaneous research notebook for the project. Record substantive hypotheses, unexpected failures, negative results, methodological changes, and next steps as they occur.

Do not rewrite old entries to make the research path look cleaner than it was. Add corrections or follow-up entries instead.

---

## Project initialization

**Date:** 2026-09-04  
**Status:** Planning

### Practical objective

Develop reusable engineering knowledge for reducing model-visible input cost in present and future software by encoding natural-language instructions visually while preserving GPT-5.6 Luna's semantic comprehension and instruction compliance.

### Research uncertainty

Publicly available benchmark evidence does not appear to establish the minimum raster density, font family, spacing, and layout at which GPT-5.6 Luna preserves natural-language instruction following under a 32×32 patch-based image-token budget.

Existing tiny-text/code-oriented tests are not sufficient to answer the question because exact transcription of identifiers, code, paths, or confusable characters is a stricter and different workload than understanding redundant natural-language instructions.

### Initial hypotheses

**H1 — semantic redundancy permits smaller text than exact-code OCR.**  
Natural-language instruction-following accuracy will remain near the text baseline at font sizes where exact identifier recovery has already begun to degrade.

**H2 — a proportional sans-serif may be more token-efficient than JetBrains Mono.**  
Because English prose does not require fixed-width cells, at least one proportional font will fit equivalent instructions into fewer 32×32 patches without materially reducing semantic comprehension.

**H3 — degradation will be task-class dependent.**  
Negation, conditional clauses, numeric thresholds, and restrictive words such as `only`, `except`, and `unless` may fail earlier than broad gist comprehension as raster density falls.

**H4 — geometric minimum patch count is not always the practical optimum.**  
Pathological aspect ratios may save one or more patches while reducing comprehension enough that a slightly larger, more balanced image has better effective quality per token.

**H5 — line spacing has a measurable efficiency frontier.**  
Reducing line gap will lower patch cost until glyph/line separation becomes poor enough to cause a non-linear comprehension penalty.

### Planned approach

1. Build a deterministic Python harness.
2. Use a persistent parent Codex session only as research coordinator.
3. Execute every scored observation in a fresh Codex CLI child session.
4. Use GPT-5.6 Luna only for the initial benchmark.
5. Build paired text and image conditions.
6. Prefer deterministic machine scoring.
7. Screen broad typography configurations shallowly.
8. Validate only promising configurations deeply with repetitions.
9. Preserve raw outputs and immutable run metadata.
10. Publish methods, synthetic benchmark tasks, and aggregate results.

### Initial font candidates

- JetBrains Mono
- Liberation Sans / Arial-equivalent
- Verdana if available
- DejaVu Sans
- Noto Sans
- Atkinson Hyperlegible
- one serif control

### Initial size candidates

`8, 9, 10, 11, 12, 13, 14, 16 px`

### Immediate next experiment

Implement `EXP-001-harness-validation` with a tiny task set. Confirm fresh-session isolation, Luna selection, paired text/image transport, deterministic scoring, patch accounting, and raw-result persistence before running any broad font sweep.

---

## Entry template

Copy this section for each substantive experiment or methodological change.

### EXP-002 — Full committed rendered-corpus benchmark

**Date:** 2026-09-05
**Status:** Completed
**Relevant commits:** `a9f5d88`; working-tree compatibility fix in `src/vce/codex.py`
**Run/config IDs:** dry run `runs/2026-09-05/01-45-36.835011Z`; initial smoke `runs/2026-09-05/01-45-44.335020Z`; repeated smoke `runs/2026-09-05/01-46-36.103279Z`; full run `runs/2026-09-05/01-47-58.663378Z`

#### Question / uncertainty

For the committed 1,600-image typography/task matrix, how often can GPT-5.6 Luna correctly follow the instruction when it is supplied only as a rendered PNG, and which font/size configurations show useful accuracy per estimated 32×32 image-token cost? The answer cannot be inferred from the renderer or text-only task definitions because it requires fresh model observations under the image transport condition.

#### Hypothesis

Natural-language semantic redundancy will allow substantial portions of the fixed visual corpus to remain instruction-following accurate at smaller raster sizes; proportional sans-serif configurations will provide at least some higher-accuracy/lower-token Pareto points than the fixed-width control. Negation, conditional, numeric, and exact-string control tasks are expected to be more fragile.

#### Independent variables

- Committed rendered instruction image: font family, raster size, layout, dimensions, and resulting patch/token estimate.
- Benchmark task and task category.

#### Controlled variables

- GPT-5.6 Luna model identifier (`gpt-5.6-luna`).
- Fresh `codex exec --ephemeral` child session per scored image, with no resume or inherited benchmark context.
- Neutral image wrapper, task payload, Codex invocation flags, deterministic scorer, committed PNG bytes, and manifest/task versions.
- Concurrency 4 for the full run; infrastructure-only retry policy retained by the harness.

#### Dataset / sample

- dataset version: committed `dataset/tasks.jsonl` and `rendered/all-instructions/manifest.jsonl` at `a9f5d88`.
- task count: 40 tasks represented across 1,600 rendered images.
- repetitions: one scored observation per image; 8-image smoke test is infrastructure validation and excluded from the full-corpus result.
- inclusion/exclusion rule: include every manifest image with a matching SHA-256 and one unique completed observation ID; exclude dry-run records and infrastructure failures from model-quality denominators while retaining them in raw results and reports. Do not discard valid model failures.

#### Method

First validate all 1,600 committed PNG paths and hashes with the dry-run path. Then run an 8-image real smoke test to verify fresh thread IDs, image transport, deterministic scoring, and no source-instruction text leakage. Then run the full fixed corpus with `python3 scripts/run_timestamped_rendered_corpus.py --concurrency 4`. If interrupted, resume the exact timestamped run directory and retain completed observations. The primary metric is valid-observation deterministic accuracy with a Wilson 95% interval. Secondary metrics are infrastructure-failure count, coding versus non-coding and category accuracy, font/size accuracy, patch/token efficiency, Pareto frontier, per-task robustness, and deterministic model-failure counts.

#### Results

The dry run verified all 1,600 committed PNGs and manifest hashes with no Codex calls. The corrected smoke test produced 8 valid observations with 7 passes, 1 deterministic model failure, 0 infrastructure failures, 8 unique child thread IDs, and no source-instruction leakage. The full run produced 1,600 valid observations: 1,412 passes and 188 deterministic model failures, for 88.25% accuracy (Wilson 95% CI 86.58%–89.74%). Mean estimated image tokens were 12.33375 and mean patch count was 10.278125.

The full run used `codex-cli 0.152.1`, concurrency 4, model `gpt-5.6-luna`, manifest SHA-256 `e798b9ee5d3bf74ca862ca2d2f260ab05edcce4580a2f5115854f9ad6090d68c`, and task-file SHA-256 `5dc3f006434ff33a9057dc3c3ed303ee3fbfd5ea9a24ccc1bedca7c3beb38d55`.

The strongest valid model-failure outlier was `coding_009`, which scored 0/40 because the exact-string scorer distinguishes `names.map(name => name.toUpperCase())` from the expected `names.map(x => x.toUpperCase())`. Other low-accuracy tasks included `reference_002` at 27/40 and `coding_014` at 28/40.

#### Infrastructure failures / exclusions

The first smoke attempt recorded 8 infrastructure failures because Codex CLI 0.152.1 treats `--image` as a variadic option and consumed the trailing prompt, yielding `No prompt provided via stdin.` The raw failed run was preserved. The harness was minimally corrected to place the prompt before `--image`; `pytest -q` then passed 5 tests, and the smoke test was repeated in a new run folder. The full run had 0 infrastructure failures, 0 duplicate child thread IDs, and no excluded valid model responses.

#### Interpretation

The fixed visual corpus achieved 88.25% deterministic task accuracy under the image-only instruction condition. This run supports descriptive font/size and accuracy/token comparisons in `REPORT.md`; it does not establish equivalence to a text baseline because no paired text-baseline run was part of this experiment.

#### Limitations

This is one observation per image, not a repeated confirmatory sample per task/configuration. The report's estimated image-token multiplier is a renderer estimate, and this run does not establish equivalence to a text baseline without a separate paired text-baseline experiment.

#### Next hypothesis / experiment

Run a separately versioned paired text-baseline experiment and repeat selected visual configurations across independent fresh sessions before making claims about visual-vs-text degradation or equivalence.

### EXP-003 — Reading-200 image-only corpus benchmark

**Date:** 2026-09-05
**Status:** Completed
**Relevant commit:** `e37374bb9ef5f2456d5647b3c72e5db4ad70b03c`
**Run/config IDs:** dry run `runs/2026-09-05/04-50-22.912054Z`; smoke `runs/2026-09-05/04-50-30.415825Z`; full run `runs/2026-09-05/04-51-23.404774Z`

#### Question / uncertainty

How accurately can GPT-5.6 Luna answer questions about 200 synthetic reading passages when the passage is available only as a pre-rendered 8px PNG, and how do six proportional fonts compare with the JetBrains Mono control at the same nominal raster size? This requires fresh image-only model observations because the answer is not determined by corpus metadata or text-only scoring.

#### Hypothesis

The proportional fonts will preserve reading-question accuracy with fewer 32×32 patches than the JetBrains Mono control, while passage length and category will produce meaningful task-level variation. The benchmark is descriptive and does not claim visual/text equivalence without a separate text baseline.

#### Independent variables

- Font condition: fira-sans, atkinson-hyperlegible, ibm-plex-sans, source-sans-3, inter, noto-sans, or jetbrains-mono control.
- Reading task and category.

#### Controlled variables

- GPT-5.6 Luna (`gpt-5.6-luna`) and Codex CLI invocation.
- One fresh `codex exec --ephemeral` child session per image, with a fresh temporary working directory and no resumed history.
- Committed PNG bytes, task/payload text, expected answers, normalized-scalar scorer, neutral wrapper, 8px raster size, and 1.2 image-token-per-patch estimate.
- Full-run concurrency 4, timeout 180 seconds, infrastructure retry limit 1.

#### Dataset / sample

- dataset version: `dataset/reading_200.jsonl` and `rendered/reading-200/manifest.jsonl` at commit `e37374bb9ef5f2456d5647b3c72e5db4ad70b03c`.
- task count: 200 passages; 1,400 image observations; 200 observations per font.
- repetitions: one observation per task×font image; 8-image smoke test is validation and excluded from headline results.
- inclusion/exclusion rule: include every manifest image exactly once with matching SHA-256 and a unique observation ID; exclude only genuine infrastructure failures from accuracy denominators while retaining them in raw results. Never retry valid wrong answers.

#### Method

Validate all manifest rows, task mappings, font counts, dimensions, observation IDs, paths, and PNG hashes before paid work. Run a full dry validation, then an 8-image real smoke test verifying prompt isolation, attachment, model, fresh threads, and deterministic scoring. Run all 1,400 images with the exact reading prompt: `Read the passage in the attached image and answer the question below. Return only the answer, with no explanation.\n\nQuestion:\n{payload}`. The primary metric is deterministic normalized-scalar accuracy with a Wilson 95% interval. Secondary metrics are latency, infrastructure failures, per-font accuracy/CI/patches/estimated tokens, category and font×category results, task robustness, JetBrains control comparison, and the accuracy/token Pareto frontier.

#### Results

The full dry validation verified all 1,400 manifest rows and PNG hashes with no Codex calls. The separate 8-image smoke test produced 8 valid observations, 6 passes, 2 deterministic model failures, 0 infrastructure failures, 8 unique child thread IDs, and no source-passage leakage. The full run produced exactly 1,400 valid observations: 612 passes and 788 deterministic model failures, for 43.7143% accuracy (Wilson 95% CI 41.14%–46.33%). Mean latency was 9,271 ms; mean patch count was 33.29; mean estimated image tokens were 39.95.

Per-font accuracy was: JetBrains Mono control 54.00% (108/200; 54.52 mean estimated tokens), Fira Sans 53.00% (106/200; 42.37 tokens), Inter 51.50% (103/200; 46.97 tokens), Source Sans 3 41.50% (83/200; 30.30 tokens), IBM Plex Sans 37.50% (75/200; 36.38 tokens), Noto Sans 35.00% (70/200; 38.36 tokens), and Atkinson Hyperlegible 33.50% (67/200; 30.73 tokens). The descriptive accuracy/token Pareto frontier was Source Sans 3, Fira Sans, and JetBrains Mono. No proportional candidate exceeded the JetBrains control overall; Fira Sans was closest (-1.00 percentage point, paired mean delta -0.010).

Category accuracy was reading_date 83.21% (233/280), reading_fact 71.07% (199/280), reading_quantity 62.14% (174/280), reading_location 2.14% (6/280), and reading_cause 0.00% (0/280). Across tasks, 74 passed on 0/7 fonts and 15 passed on all 7 fonts; the full 0–7 distribution is recorded in `REPORT.md`. Category×font results, Wilson intervals, control pairing, and failure accounting are in the full report.

#### Infrastructure failures / exclusions

There were 0 final infrastructure failures and no excluded observations: all 1,400 task×font observations completed and were scored. Two observations (`reading_012`/`ibm-plex-sans` and `reading_151`/`ibm-plex-sans`) have `attempts=2`, indicating one infrastructure retry before a final valid response. Valid wrong answers were not retried. The run used 1,400 unique nonempty child thread IDs, and every final invocation was recorded with `--ephemeral`, the Luna model, the exact image-only prompt, and the assigned PNG.

#### Interpretation

At this fixed 8px raster size, the control had the highest overall accuracy, while Fira Sans was the strongest proportional candidate and Source Sans 3 was the lowest-token Pareto point. The category pattern is highly uneven, with date/fact questions substantially stronger than cause/location questions across fonts. These are descriptive image-only results; they do not establish text-baseline savings or equivalence.

#### Limitations

One observation per task×font is exploratory rather than repeated confirmation. The estimated image-token multiplier is a configured estimate, not a billing measurement.

#### Next hypothesis / experiment

Repeat selected task×font conditions across independent fresh sessions and run a separately versioned paired text baseline before making claims about visual-versus-text degradation, equivalence, or savings.

### EXP-004 — Paired Reading-200 text baseline and Fira Sans size sweep

**Date:** 2026-09-05
**Status:** Completed
**Relevant commit:** `752a0fd6a47c1392e750112de11fa7a0cc4b8355`
**Run/config IDs:** smoke `runs/2026-09-05/16-26-48.799642Z`; full `runs/2026-09-05/16-28-30.490211Z`

#### Question / uncertainty

How does image-only reading accuracy change from 8px to 12px Fira Sans relative to a plain-text baseline on the exact same 200 synthetic reading tasks? The prior 8px multi-font benchmark had no paired text baseline, so it could not quantify the accuracy gap or determine whether larger renders approach text performance.

#### Hypothesis

Increasing Fira Sans from 8px to 12px will improve image accuracy and recover some tasks that fail at 8px; the text baseline will remain the strongest condition. Cause and location questions are expected to be especially fragile at small sizes.

#### Independent variables

- Input condition: original passage as text or passage supplied only through the committed Fira Sans PNG.
- Image raster size: 8px, 9px, 10px, 11px, or 12px.
- Reading task and category.

#### Controlled variables

- Exact dataset SHA-256 `987988ff39e3ed843ec1b6bb0b6287415c4cbfea83edf6ca4c60a7a25b6f1aef` and committed PNG bytes at `752a0fd6`.
- GPT-5.6 Luna only, deterministic normalized-scalar scorer, one fresh `codex exec --ephemeral` child per observation, and no valid-response retries.
- Same question payload, concurrency 4, timeout 180 seconds, and infrastructure retry limit 1.

#### Dataset / sample

- 200 tasks; 1,000 image observations (Fira Sans × five sizes) plus 200 text-baseline observations.
- One observation per task×condition; smoke observations are excluded from headline results.
- Include every committed image with a valid SHA-256 and every text task; exclude only final infrastructure failures from accuracy denominators while retaining them in raw evidence.

#### Method

Validate all 1,000 committed PNGs and the unchanged dataset before paid execution. Run a small paired smoke test, then the complete 1,200-observation run with the existing fresh-child mechanism. The image prompt is the fixed image-only wrapper plus question; the text prompt contains the original passage and the same question without the expected answer. Report Wilson intervals, latency, observed text input tokens when available, category and task recovery, and image accuracy/token Pareto results.

#### Results

The preflight verified the unchanged dataset SHA-256 `987988ff39e3ed843ec1b6bb0b6287415c4cbfea83edf6ca4c60a7a25b6f1aef`, 200 tasks, 1,000 Fira Sans PNGs, 200 images at each size from 8px through 12px, unique observation IDs, and all 1,000 image hashes. The paired smoke test completed 6/6 observations (one task at all five sizes plus text), with six unique child threads, exact prompt/attachment checks, and no infrastructure failures.

The full run completed exactly 1,200 observations: 200 text and 1,000 image. The plain-text baseline passed 125/200 = 62.50% (Wilson 95% CI 55.61%–68.91%) with mean recorded Codex input tokens 13,302.80 (range 13,006–14,339). Image accuracy was 8px 102/200 = 51.00% (44.12%–57.84%), 9px 110/200 = 55.00% (48.08%–61.74%), 10px 114/200 = 57.00% (50.07%–63.67%), 11px 104/200 = 52.00% (45.10%–58.82%), and 12px 104/200 = 52.00% (45.10%–58.82%). Mean estimated image tokens were 42.37, 47.66, 60.87, 66.80, and 82.58 respectively; the accuracy gaps versus text were -11.50, -7.50, -5.50, -10.50, and -10.50 percentage points. The 10px condition was closest to the text baseline.

The image accuracy/token Pareto frontier was 8px, 9px, and 10px; 11px and 12px were dominated by lower-token conditions. Task recovery from 8px to 12px had 19 recovered tasks, 17 regressions, 85 stable passes, and 79 stable failures. Cause accuracy remained 0.00% at every size and in text; location accuracy was 5.00% at 8px, 2.50% at 9px and 10px, and 5.00% at 11px and 12px, versus 12.50% for text. Date/fact/quantity categories peaked at 10px but did not monotonically improve through 12px. Full category tables, all task transitions, latency, tokens, and raw evidence are in `REPORT.md`.

#### Infrastructure failures / exclusions

There were 0 final infrastructure failures, 0 infrastructure-retry rows, and no excluded observations. All 1,200 final rows used `gpt-5.6-luna`, unique fresh child threads, and one attempt; valid wrong answers were not retried. The paired coordinator and report were added as the necessary harness extension because the existing rendered-corpus runner handled only image manifests and could not represent the paired text condition. A smoke-only report category assumption and resume run-ID bookkeeping issue were corrected without rerunning scored rows.

#### Interpretation

The 10px Fira Sans image condition was the closest to the plain-text baseline but remained 5.50 percentage points lower; its Wilson interval overlaps the baseline interval, but this single observation per task/condition is not an equivalence test. Increasing size above 10px did not improve accuracy and increased estimated image-token cost, so the observed frontier favors 8–10px for this corpus. Persistent cause/location weakness appears task- or dataset-specific rather than resolved by larger raster text. No text/image equivalence or savings claim is made.

#### Limitations

One observation per task×condition is exploratory rather than repeated confirmation. Codex-reported text input tokens include the model's recorded input accounting and may include wrapper/system overhead; estimated image tokens are renderer estimates.

#### Next hypothesis / experiment

Repeat selected task×size conditions across independent fresh sessions and investigate the cause/location task construction before changing the dataset or scoring. A future text/image comparison should predeclare an equivalence margin if equivalence is the intended claim.

### EXP-XXX — Title

**Date:** YYYY-MM-DD  
**Status:** Planned | Running | Completed | Aborted  
**Relevant commits:**  
**Run/config IDs:**  

#### Question / uncertainty

What is not known and why can it not be answered from the existing results?

#### Hypothesis

State a falsifiable prediction before viewing the new results.

#### Independent variables

- ...

#### Controlled variables

- ...

#### Dataset / sample

- dataset version:
- task count:
- repetitions:
- inclusion/exclusion rule:

#### Method

Describe the planned run and scoring procedure.

#### Results

Include both positive and negative results. Link or identify raw and aggregate outputs.

#### Infrastructure failures / exclusions

Record counts and reasons. Do not merge infrastructure failures into model-error rates.

#### Interpretation

What did the experiment establish, fail to establish, or make less likely?

#### Limitations

What alternative explanations remain?

#### Next hypothesis / experiment

State the next question generated by this result.

---

## Change-log rule

If methodology, scoring, task composition, model selection, or rendering assumptions change materially, add a dated entry here and increment the affected experiment/dataset/configuration version rather than silently modifying the interpretation of old results.
