# Parent Codex prompt — run the full rendered benchmark

Use the following prompt in the persistent parent Codex research-coordinator session when you are ready to run the committed image corpus:

```text
Run the complete pre-rendered Visual Context Efficiency benchmark using the committed corpus under rendered/all-instructions/.

First verify that rendered/all-instructions/manifest.jsonl exists, that every image referenced by the manifest exists, and that its SHA-256 matches the manifest. Do not regenerate or modify the images for this run.

Use scripts/run_rendered_corpus.py with GPT-5.6 Luna. Every scored image must be sent to a fresh child Codex session using codex exec --ephemeral. Never use codex resume, a previous thread ID, or inherited benchmark history for a scored observation. The source instruction must not be duplicated as text. Each child should receive only the neutral wrapper, the task payload, and its assigned instruction image.

Before the full run, execute a dry run over the complete corpus and then a small real smoke test of 8 images. Inspect the smoke-test raw JSONL and confirm that fresh thread IDs are present, image hashes match, deterministic scoring works, and no source instruction leaked into the child text prompt. If the smoke test reveals an infrastructure problem, fix the harness and repeat the smoke test before continuing.

Then run all 1,600 rendered images. Use a conservative concurrency level of 4 unless rate limits or local resource constraints indicate a lower value. Infrastructure failures may be retried according to the harness policy; valid model responses must never be retried because they scored poorly. If the run is interrupted, resume the same run directory rather than starting those completed observations again.

After completion, verify that the run contains exactly 1,600 unique completed observation IDs and no duplicate child thread IDs. Generate and inspect results.csv, results.jsonl, summary.json, and REPORT.md. REPORT.md should include overall accuracy and Wilson 95% confidence interval; coding versus non-coding performance; per-category, per-font, per-size, and font-by-size results; patch and estimated image-token efficiency; an empirical accuracy/token Pareto frontier; per-task robustness; deterministic model failures; and infrastructure failures.

Do not characterize the result as statistically equivalent to the text baseline unless a separate paired text-baseline experiment supports that conclusion. Record the run ID, current git commit, Codex CLI version, model, manifest hash, task-file hash, and any anomalies in RESEARCH_LOG.md after the run.

Use these commands unless repository changes make an equivalent command necessary:

python scripts/run_rendered_corpus.py --dry-run
python scripts/run_rendered_corpus.py --limit 8 --concurrency 2
python scripts/run_rendered_corpus.py --concurrency 4

If a full run is interrupted, resume with:

python scripts/run_rendered_corpus.py --resume runs/<run-id> --concurrency 4
```

The parent coordinator may inspect outputs and fix genuine harness/infrastructure problems, but it must not directly answer any scored benchmark item.
