# Contributing

Contributions are welcome, especially improvements that make the benchmark more reproducible, better controlled, or more representative of real instruction-following workloads.

## Scope

The initial benchmark targets **GPT-5.6 Luna** and studies visual encoding of natural-language instructions. Please avoid turning the project into a broad model leaderboard unless that scope is explicitly changed in a documented research phase.

Useful contributions include:

- synthetic benchmark tasks;
- deterministic scorers;
- renderer improvements;
- reproducibility fixes;
- Codex CLI isolation checks;
- statistical analysis;
- additional font/rendering configurations;
- documentation corrections; and
- replication results.

## Experimental integrity

Any scored benchmark contribution must follow the repository methodology:

- fresh child Codex session per scored observation;
- no resumed benchmark history;
- exact model recorded;
- paired text/image design where applicable;
- source instruction not duplicated as text in image conditions;
- raw response preservation;
- predeclared scoring rules;
- infrastructure failures separated from model failures; and
- complete rendering/run metadata.

Do not selectively rerun valid responses because they are inconvenient or score poorly.

## Reproducibility

A contributed result should identify:

- experiment ID;
- dataset version/commit;
- harness commit;
- configuration file/hash;
- model identifier;
- Codex CLI version if available;
- font family and font-resource identity;
- rendering parameters;
- task and repetition counts;
- inclusion/exclusion rules;
- raw-result location or reproducible archive; and
- scoring/report-generation procedure.

If exact reproduction is impossible because the hosted model changed, say so explicitly and preserve the date/environment information.

## Benchmark tasks

New public tasks should be synthetic or otherwise safe and licensed for redistribution.

Prefer tasks with deterministic expected outcomes. Do not add ambiguous instructions merely to increase difficulty; the benchmark should measure visual comprehension rather than ambiguity resolution.

Avoid datasets that expose:

- customer or user data;
- private receipts/documents;
- proprietary production prompts;
- credentials;
- unreleased business logic; or
- material without suitable redistribution rights.

## Fonts

Do not commit proprietary or restricted font binaries merely for convenience. Renderer configurations may refer to locally installed fonts and should record exact family/file metadata or hashes where legally appropriate.

Open-licensed fonts may be included later if their licences and notices are handled correctly.

## Changes to methodology

Methodological changes should be proposed and documented before being mixed with existing final results. If a change affects comparability, start a new experiment/configuration version rather than silently rescoring or relabelling prior results.

## Code quality

When code is added:

- keep orchestration explicit and inspectable;
- use versioned schemas for tasks/configs/results;
- keep rendering deterministic;
- add focused tests for scorers and token/patch calculations;
- avoid hidden global state in the trial launcher; and
- never claim a test passed unless it was actually run.

## Result claims

Phrase conclusions narrowly enough to match the evidence. Prefer:

> Under benchmark version X and the recorded GPT-5.6 Luna environment, configuration A achieved ...

rather than universal claims such as:

> Font A is always best for AI.

Negative or null results are valuable and should be retained.
