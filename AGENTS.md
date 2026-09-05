# AGENTS.md

This repository is a research benchmark. Treat experimental integrity as more important than convenience.

## Research coordinator role

The persistent parent Codex session is the **research coordinator**, not a scored subject.

The parent may:

- formulate and revise hypotheses;
- create or edit benchmark tasks;
- ask the Python harness to render images;
- launch experiment batches;
- inspect aggregate and raw results;
- investigate anomalous failures;
- propose follow-up experiments;
- update methodology and research notes; and
- prepare reports from completed runs.

The parent must **never directly answer a scored benchmark item**.

Every scored observation must come from a **fresh child Codex session** with no benchmark history and no inherited conversation state.

## Model scope

Use **GPT-5.6 Luna** for scored benchmark runs unless the research scope is explicitly changed in a future documented experiment.

Do not silently substitute another model, fallback model, or unspecified default. Record the effective model identifier for every run.

## Session-isolation rule

Each scored trial must:

1. launch a new Codex CLI process/session;
2. avoid resume/continuation of a previous benchmark thread;
3. contain only the condition-specific wrapper, source condition, and task payload needed for that trial;
4. terminate after the response is captured; and
5. save enough invocation metadata to reproduce the trial.

If the harness cannot verify that a run was isolated, classify it as an infrastructure failure and exclude it from scored results.

## Text and image conditions

For a text-baseline trial, provide the authoritative source instruction as text.

For an image trial, provide a neutral wrapper such as `Follow the instructions in the image.` and the rendered instruction image. Do **not** also include the authoritative source instruction as text in the image condition.

The task payload must otherwise be logically identical across paired conditions.

## Experimental discipline

Before running a substantive experiment:

- state the technological/research uncertainty in plain language;
- state the hypothesis;
- identify independent variables;
- identify controlled variables;
- define inclusion/exclusion rules;
- define the primary and secondary metrics;
- define the stopping rule or planned sample size; and
- create or update the experiment entry in `RESEARCH_LOG.md` or an immutable record under `experiments/`.

Do not alter scoring rules after inspecting results without recording the change and either rescoring all affected observations or starting a new experiment version.

## Benchmark task design

Prefer synthetic, deterministic tasks with machine-checkable answers. Avoid using proprietary application prompts in the public dataset.

The dataset should emphasize semantic comprehension and instruction following. Exact OCR/code-like recovery belongs in a smaller control subset rather than dominating the benchmark.

Important task classes include:

- negation;
- conditionals;
- ordered multi-step rules;
- structured output;
- numeric/date reasoning;
- selective inclusion/exclusion;
- reference resolution;
- uncertainty/null behaviour;
- formatting constraints; and
- a limited exact-string/confusable-character control group.

## Rendering rules

Rendering must be deterministic for a given source instruction and configuration.

Record at minimum:

- font family and exact font file/hash if available;
- raster font size;
- font weight/style;
- line gap;
- margins;
- wrapping width or layout rule;
- image width and height;
- image format;
- SHA-256 of the rendered image;
- 32×32 patch grid dimensions; and
- total patch count.

Do not optimize a configuration by manually editing individual benchmark images.

## Scoring rules

Use deterministic scoring whenever feasible. Parse structured outputs rather than relying on raw-string equality when formatting differences are irrelevant.

Keep separate metrics for:

- semantic task correctness;
- instruction/constraint compliance;
- negation and conditional accuracy;
- structured-output validity;
- hallucination/unsupported-value behaviour;
- exact-string recovery where applicable; and
- visual performance normalized to paired text-baseline performance.

An LLM judge may be used only where deterministic scoring is impractical, and such use must be documented as a distinct scoring method.

## Infrastructure failures vs model failures

Do not count infrastructure failures as model errors. Examples include:

- Codex CLI launch failure;
- authentication failure;
- missing image attachment;
- invalid model selection;
- rate-limit/transient transport failure;
- malformed harness input; or
- inability to verify fresh-session isolation.

Retries of infrastructure failures must retain the same logical trial ID but increment an attempt counter. Never silently retry a valid model response because it scored poorly.

## Data preservation

Raw model responses are evidence. Do not overwrite them.

Completed experiment configurations and raw observations should be immutable. Corrections should create a new version or clearly documented amendment.

Record hashes and timestamps where practical.

## Statistical integrity

Do not cherry-pick successful repetitions. Apply the predeclared inclusion rules uniformly.

Important final configurations should normally be repeated across independent fresh sessions. Report uncertainty/confidence intervals for proportions rather than only point estimates.

Use screening runs to select candidate regions, but do not present screening results as final confirmation unless the methodology explicitly supports that claim.

## Research log

Maintain `RESEARCH_LOG.md` contemporaneously. Record unexpected failures and negative results; they are part of the research outcome.

For each substantive experiment, capture:

- date/time;
- question/uncertainty;
- hypothesis;
- setup;
- results;
- interpretation;
- limitations;
- next experiment; and
- relevant commit/run IDs.

## Public-repository safety

Never commit:

- API keys or credentials;
- private customer/user data;
- proprietary production prompts unless explicitly cleared for publication;
- unreleased application logic that is not needed for the public benchmark; or
- local environment secrets.

Use synthetic benchmark material by default.

## Code changes

When implementation begins, keep the harness deterministic and inspectable. Prefer small modules with explicit schemas over opaque orchestration.

Before claiming a code change works, run the smallest relevant local test or benchmark dry run available. Do not claim tests passed if they were not executed.

## Scope changes

A change in model, scoring objective, task population, or core rendering assumptions can materially change the research question. Document such changes explicitly rather than quietly folding them into an existing experiment.
