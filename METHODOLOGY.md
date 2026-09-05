# Methodology

## Objective

Measure how typography and raster layout affect GPT-5.6 Luna's ability to understand and follow natural-language instructions when those instructions are supplied visually rather than as text.

The benchmark is designed to separate three questions that are often conflated:

1. **Can the model read the characters?**
2. **Can the model recover the intended meaning?**
3. **Can the model follow the instruction correctly?**

The primary benchmark target is (3), with (1) and (2) retained as diagnostic dimensions.

## Experimental unit

A scored observation is one fresh Codex CLI child session answering one benchmark task under one condition.

A logical task may have multiple observations because it can be tested as:

- a text baseline;
- one or more image-rendering configurations; and
- repeated independent runs.

The persistent parent Codex session is not an experimental unit and must not answer scored items.

## Paired-condition design

Every image condition should be paired with the same logical task in text form.

### Text baseline

Input contains the source instruction as ordinary text and the task payload.

### Image condition

Input contains a neutral wrapper, such as `Follow the instructions in the image.`, the rendered source instruction, and the same task payload.

The image condition must not receive the source instruction in text form.

This paired design controls for the fact that some tasks may be intrinsically difficult for Luna even without a visual-reading burden.

## Independent variables

Initial independent variables:

- font family;
- font size in raster pixels;
- line gap;
- margin size;
- text wrapping width / image aspect ratio; and
- later, font weight and layout strategy.

Only a small, interpretable set of variables should be changed in any single experiment.

## Controlled variables

Unless explicitly under test, keep constant:

- GPT-5.6 Luna model selection;
- Codex CLI invocation pattern;
- fresh-session policy;
- neutral image-condition wrapper;
- task payload;
- source instruction wording;
- image foreground/background colours;
- image format;
- renderer and antialiasing behaviour;
- scoring rules;
- retry policy; and
- reasoning/temperature-style settings where controllable.

## Rendering and token accounting

For a rendered image of width `W` and height `H`, always record the geometric 32×32 patch grid:

```text
patch_columns = ceil(W / 32)
patch_rows    = ceil(H / 32)
patch_count   = patch_columns * patch_rows
```

Model-billed image tokens must be reported using the model-specific rule verified for the experiment. The calculation and its source/version should be recorded rather than assumed forever.

Do not use compressed PNG byte size as a proxy for model token cost.

## Font-size convention

Font size must be specified in actual renderer raster pixels, not CSS points or ambiguous display sizes. Record the rendering library and exact font resource/hash where practical.

If a font is not redistributable, do not commit the font file. Record sufficient metadata for another user to supply an equivalent local installation.

## Task population

The benchmark should contain mostly semantic/instruction-following tasks and a smaller exact-OCR control subset.

Task construction requirements are defined in `BENCHMARK_TASKS.md`.

The final validation set should not be repeatedly edited in response to observed typography results. Changes to tasks or expected outputs require a dataset version bump.

## Scoring hierarchy

Prefer, in order:

1. exact deterministic programmatic scoring;
2. normalized parsing plus deterministic comparison;
3. rule-based partial scoring;
4. an explicitly documented LLM judge only when necessary.

Examples:

- JSON tasks should be parsed and compared by field semantics rather than whitespace.
- `lowercase only` or `exactly three items` constraints should have dedicated compliance checks.
- Numeric answers should define allowed representation/tolerance before the run.
- Null/unknown behaviour should be scored distinctly from ordinary correctness.

## Core metrics

### Task correctness

Whether the model produced the logically correct answer.

### Constraint compliance

Whether it obeyed format, count, ordering, exclusion, or response-shape rules.

### Negation accuracy

Accuracy on tasks where `not`, `except`, `exclude`, `never`, or equivalent qualifiers alter the answer.

### Conditional accuracy

Accuracy on `if`, `unless`, `otherwise`, threshold, or branch rules.

### Hallucination rate

Frequency of outputs containing values explicitly unsupported by the task material when the correct behaviour is null, omission, or uncertainty.

### Exact-string accuracy

Used for the smaller OCR-control subset involving identifiers, punctuation, case, or confusable characters.

### Text-baseline-normalized performance

For an aggregate score `S`:

```text
normalized_visual_score = S_image / S_text
```

If the text score is zero for a task or stratum, do not divide blindly; report the task separately or use a predeclared aggregate treatment.

### Token efficiency

Report at least:

```text
semantic_score / image_input_tokens
```

and, where meaningful:

```text
relative_token_saving = 1 - image_input_tokens / equivalent_text_input_tokens
```

The latter should not be interpreted as useful if visual quality falls below the predefined quality threshold.

## Pareto-frontier analysis

A rendering configuration is dominated if another tested configuration has:

- equal or better semantic/instruction-following quality; and
- lower or equal token cost;

with at least one strict improvement.

The practical goal is to identify the non-dominated frontier and then choose the lowest-cost configuration whose quality is statistically and operationally acceptable.

## Screening vs confirmation

### Screening

Broad font/size sweeps may use fewer tasks and fewer repetitions to locate promising regions. These results are exploratory.

### Confirmation

Candidate configurations should be tested on a larger task set with independent repetitions and predeclared scoring before being reported as final findings.

The same observations should not be used both to tune the benchmark and to claim unbiased final confirmation without acknowledging that dependence.

## Repetitions

For important final configurations, use at least three independent fresh-session observations per task unless a later power analysis supports a different design.

Do not discard a valid response because it is an outlier or scores poorly.

## Confidence intervals

For binary success proportions, report Wilson intervals or another documented binomial interval rather than only raw percentages.

For composite metrics, report the aggregation method and uncertainty procedure explicitly. Bootstrap intervals are acceptable when the resampling unit preserves task-level dependence.

## Model and environment drift

Because hosted models and client software can change, long-running studies should interleave or periodically rerun text baselines and a small fixed visual control panel.

Record:

- UTC timestamp;
- model identifier;
- Codex CLI version/commit if available;
- harness commit;
- dataset version;
- renderer version; and
- configuration hash.

A material environment change should begin a new experiment phase or be treated as a blocking factor in analysis.

## Randomization

Where practical, randomize task order and configuration order within a batch so time-of-run effects are not perfectly confounded with one font or size.

Use a recorded random seed when the harness generates a randomized schedule.

## Infrastructure failures

Infrastructure failures are excluded from model-quality denominators and tracked separately.

Examples:

- process launch failure;
- network/authentication failure;
- invalid/missing image;
- wrong effective model;
- corrupted payload;
- rate-limit error; or
- failed isolation check.

Retry only infrastructure failures. A valid model answer, even a bad one, is an observation and must not be retried selectively.

## Stopping and sample-size discipline

Each confirmatory experiment should state its planned task count and repetitions before launch. If a run is stopped early, record why.

Exploratory screening may be adaptive, but the adaptation logic should be documented in the research log.

## Data integrity

Raw responses and completed run configurations should be append-only in normal operation. If a parser/scorer bug is found, preserve the original raw outputs and create a new scoring version.

At minimum, each observation should store:

```json
{
  "experiment_id": "...",
  "task_id": "...",
  "dataset_version": "...",
  "condition": "text|image",
  "model": "gpt-5.6-luna",
  "font": "...",
  "font_size_px": 0,
  "line_gap_px": 0,
  "image_width": 0,
  "image_height": 0,
  "patch_columns": 0,
  "patch_rows": 0,
  "patch_count": 0,
  "image_token_rule": "...",
  "image_tokens": 0,
  "image_sha256": "...",
  "instruction_sha256": "...",
  "attempt": 1,
  "response": "...",
  "expected": "...",
  "score": {},
  "latency_ms": 0,
  "exit_code": 0,
  "timestamp_utc": "..."
}
```

Fields irrelevant to a text condition may be null rather than omitted if that simplifies the schema.

## Interpretation rule

A smaller font is not automatically better. The preferred configuration is the one that minimizes model-visible token cost **subject to an explicit comprehension/compliance threshold**.

A result such as `11 px saves 25% of image tokens` is incomplete unless accompanied by the corresponding semantic and constraint-following performance.
