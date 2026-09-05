# Experiment Plan

This document defines the initial execution plan for the GPT-5.6 Luna visual-instruction benchmark.

## Phase 0 — repository and harness specification

Before any scored benchmark run, implement or document:

- task schema;
- rendering configuration schema;
- run-result schema;
- fresh-session Codex CLI launcher;
- model-verification check where possible;
- image renderer;
- patch/token accounting;
- deterministic scorers;
- infrastructure-failure classifier;
- immutable raw-output storage; and
- experiment configuration hashing.

Success criterion: a dry run can execute one text baseline and one image condition for the same task in independent fresh sessions and produce complete, machine-readable metadata.

## Phase 1 — harness validation

Use approximately 8–12 deliberately simple tasks.

Goals:

1. prove every scored call is a fresh child session;
2. verify the parent coordinator is not included in child context;
3. verify the selected model is GPT-5.6 Luna;
4. verify the image arrives and is readable;
5. verify the text and image task payloads are otherwise equivalent;
6. verify stdout/stderr and exit status capture;
7. verify deterministic scoring;
8. verify transient failures are retried without retrying poor valid answers; and
9. verify run records are append-only.

Do not include Phase 1 observations in headline benchmark results.

## Phase 2 — broad typography screening

### Research question

Which font-family/font-size regions preserve high semantic instruction following while substantially reducing patch count?

### Initial hypothesis

Natural-language instructions will tolerate smaller raster sizes than code-like exact-recall tasks because lexical and semantic context provides redundancy. At equal semantic quality, at least one proportional sans-serif font is expected to use fewer patches than JetBrains Mono.

### Fonts

Initial set:

1. JetBrains Mono
2. Liberation Sans or Arial-equivalent
3. Verdana, if legally/locally available
4. DejaVu Sans
5. Noto Sans
6. Atkinson Hyperlegible
7. Liberation Serif or another readable serif control

If a font is unavailable, record the substitution before the run rather than silently changing the set.

### Sizes

Test:

```text
8, 9, 10, 11, 12, 13, 14, 16 px
```

### Other rendering controls

Keep fixed initially:

- regular weight;
- black text on white;
- PNG;
- deterministic antialiasing;
- minimal fixed margins;
- one fixed line gap, initially 1 px;
- deterministic word wrapping; and
- one declared layout-width optimization rule.

### Task sample

Use 30–40 tasks stratified across the task classes in `BENCHMARK_TASKS.md`.

Do not make the screening sample mostly exact-string tasks.

### Repetitions

One observation per task/configuration is acceptable for the first broad screen, because the objective is candidate elimination rather than final inference.

### Outputs

For each font/size configuration calculate:

- semantic correctness;
- constraint compliance;
- negation/conditional subgroup accuracy;
- hallucination rate;
- exact-string control accuracy;
- median and distribution of patch counts;
- mean/median reported image input tokens; and
- normalized performance relative to paired text baselines.

### Candidate selection

Select roughly 5–8 configurations for Phase 3 based primarily on the quality/token Pareto frontier.

Do not select solely by the single lowest patch count.

## Phase 3 — focused validation

### Purpose

Measure the best candidate configurations with enough task diversity and repetition to distinguish real quality differences from run noise.

### Task count

Target 150–200 versioned tasks.

### Repetitions

Target three independent fresh child sessions per task/configuration.

Run text baselines in fresh sessions as well. If API budget is a concern, the exact baseline repetition plan may be changed before execution, but it must be recorded in the experiment configuration.

### Primary outcome

Determine the lowest-token configuration that preserves a predefined fraction of text-baseline instruction-following performance.

Before launching this phase, choose and record the operational threshold. Example only:

```text
>= 99% of paired text-baseline semantic/constraint performance
```

The final threshold should be justified and must not be changed after seeing the final results without creating a new analysis version.

### Statistical reporting

Report:

- task-level and observation-level counts;
- success rates;
- Wilson intervals for binary outcomes;
- per-task paired differences where appropriate;
- subgroup performance;
- token-cost distributions; and
- Pareto dominance.

## Phase 4 — line spacing and vertical density

After selecting promising font/size combinations, test line gaps such as:

```text
0 px, 1 px, 2 px, 3 px
```

Research question: does removing vertical whitespace reduce patch cost without creating a disproportionate semantic-comprehension penalty?

Hold font, size, task set, and other variables constant.

## Phase 5 — width and aspect-ratio optimization

For a fixed amount of text, patch count depends on both wrapping and 32×32 boundary rounding.

Test layout policies such as:

- approximately square;
- minimum geometric patch count;
- maximum width constraints (for example 384, 512, 768 px);
- moderate landscape;
- moderate portrait; and
- optional multi-column layout if single-column results justify testing it.

Avoid pathological ultra-wide or ultra-tall layouts unless they are being tested explicitly as controls.

Measure not only patch count but semantic quality; a one-patch geometric saving is not useful if the layout harms comprehension.

## Phase 6 — font weight and glyph density

Test regular versus medium/bold only after size and layout have been narrowed.

Questions:

- Does a slightly heavier glyph permit a smaller font size with equal comprehension?
- Does the added stroke thickness reduce readability when tightly packed?
- Is a heavier small font more token-efficient than a larger regular font?

## Phase 7 — failure-cliff mapping

Take the best few configurations and test densely around their transition region.

Example:

```text
9, 10, 11, 12 px
```

with larger task counts and repetitions.

Identify whether degradation is gradual or whether certain semantic classes fail abruptly.

Pay particular attention to:

- negation;
- conditional clauses;
- `only`/`except` restrictions;
- numeric thresholds;
- null/unknown rules; and
- structured-output requirements.

## Phase 8 — real-world-shaped synthetic tasks

After the generic benchmark is stable, create public synthetic tasks resembling real software instruction patterns without disclosing proprietary prompts.

Examples:

- receipt extraction schema rules;
- document classification;
- data-normalization instructions;
- API response transformation;
- agent task constraints; and
- compact context summaries.

Use these as an external-validity layer, not as a replacement for the general benchmark.

## Experiment naming

Use immutable IDs such as:

```text
EXP-001-harness-validation
EXP-002-font-size-screen
EXP-003-focused-font-validation
EXP-004-line-gap
EXP-005-layout-width
```

Each completed experiment should have a record under `experiments/` containing:

- question;
- hypothesis;
- exact config/hash;
- dataset version;
- run IDs;
- exclusions and infrastructure failures;
- results;
- interpretation;
- limitations; and
- next experiment.

## Suggested first implementation milestone

The first coding milestone should **not** attempt the entire benchmark. Build enough to execute:

```text
1 task
× 1 text baseline
× 2 image fonts
× 2 image sizes
× 1 fresh child session per condition
```

Verify the resulting records manually. Then expand to Phase 1.

## Cost-control strategy

Use staged elimination:

- cheap/small harness validation;
- broad but shallow screening;
- deeper repetitions only on promising candidates.

Do not reduce research quality by reusing scored Codex sessions. Session isolation is a core control and should not be traded away for call savings.

## Decision criterion

The project should ultimately be able to state a result in a form like:

> For GPT-5.6 Luna under benchmark version X, configuration A retained Y% of paired text-baseline instruction-following quality at Z image input tokens, and no tested lower-token configuration met the predefined quality threshold.

Any conclusion must name the dataset version, date/model environment, rendering configuration, and uncertainty.
