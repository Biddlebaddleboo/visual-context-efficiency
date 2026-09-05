#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import secrets
import statistics
import threading
from typing import Any

from vce.codex import codex_version, result_dict, run_fresh
from vce.dataset import load_tasks
from vce.scoring import score_response


DEFAULT_PROMPT_TEMPLATE = "Follow the instructions in the attached image.\n\nTask payload:\n{payload}"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"rendered-corpus-{stamp}-{secrets.token_hex(4)}"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total <= 0:
        return (0.0, 0.0)
    p = successes / total
    z2 = z * z
    denom = 1.0 + z2 / total
    centre = (p + z2 / (2.0 * total)) / denom
    margin = z * math.sqrt((p * (1.0 - p) + z2 / (4.0 * total)) / total) / denom
    return (max(0.0, centre - margin), min(1.0, centre + margin))


def safe_mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def load_manifest(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise ValueError(f"manifest is empty: {path}")
    required = {"task_id", "font_id", "font_size_px", "patches", "estimated_image_tokens", "image_sha256", "path"}
    for i, row in enumerate(rows, start=1):
        missing = required - row.keys()
        if missing:
            raise ValueError(f"manifest row {i} missing fields: {', '.join(sorted(missing))}")
    return rows


def resolve_image_path(manifest_path: Path, row: dict[str, Any]) -> Path:
    raw = Path(str(row["path"]))
    candidates = [raw]
    if not raw.is_absolute():
        candidates.append(Path.cwd() / raw)
        candidates.append(manifest_path.parent / raw.name)
        # The committed corpus uses manifest parent/font/size/task.png.
        candidates.append(
            manifest_path.parent
            / str(row["font_id"])
            / f"{row['font_size_px']}px"
            / f"{row['task_id']}.png"
        )
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError(f"image not found for task={row['task_id']} font={row['font_id']} size={row['font_size_px']}: {raw}")


def load_completed(path: Path) -> dict[str, dict[str, Any]]:
    completed: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return completed
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        observation_id = row.get("observation_id")
        if isinstance(observation_id, str):
            completed[observation_id] = row
    return completed


def make_observation_id(row: dict[str, Any]) -> str:
    return f"{row['task_id']}:{row['font_id']}:{row['font_size_px']}px:{row['image_sha256'][:12]}"


def is_coding(task: Any) -> bool:
    return str(task.category).casefold() == "coding" or any(str(tag).casefold() == "coding" for tag in task.tags)


def run_one(
    *,
    manifest_row: dict[str, Any],
    image_path: Path,
    task: Any,
    model: str,
    codex_bin: str,
    timeout: int,
    infra_retries: int,
    prompt_template: str,
) -> dict[str, Any]:
    observation_id = make_observation_id(manifest_row)
    prompt = prompt_template.format(payload=task.payload)
    attempts = 0
    result = None

    while attempts <= infra_retries:
        attempts += 1
        result = run_fresh(
            prompt,
            image=image_path,
            model=model,
            codex_bin=codex_bin,
            timeout_seconds=timeout,
        )
        if result.infrastructure_failure is None:
            break

    assert result is not None
    scoring = None
    if result.infrastructure_failure is None:
        scoring = score_response(result.response, task.expected, task.scorer)

    return {
        "observation_id": observation_id,
        "completed_at": utc_now(),
        "task_id": task.task_id,
        "task_version": task.version,
        "category": task.category,
        "workload": "coding" if is_coding(task) else "noncoding",
        "tags": list(task.tags),
        "instruction_sha256": sha256_text(task.instruction),
        "payload_sha256": sha256_text(task.payload),
        "expected": task.expected,
        "scorer": task.scorer,
        "font_id": manifest_row.get("font_id"),
        "font_family": manifest_row.get("font_family"),
        "font_size_px": manifest_row.get("font_size_px"),
        "margin_px": manifest_row.get("margin_px"),
        "line_gap_px": manifest_row.get("line_gap_px"),
        "width": manifest_row.get("width"),
        "height": manifest_row.get("height"),
        "patch_columns": manifest_row.get("patch_columns"),
        "patch_rows": manifest_row.get("patch_rows"),
        "patches": manifest_row.get("patches"),
        "estimated_image_tokens": manifest_row.get("estimated_image_tokens"),
        "font_sha256": manifest_row.get("font_sha256"),
        "image_sha256": manifest_row.get("image_sha256"),
        "image_path": str(image_path),
        "model": model,
        "prompt_template_sha256": sha256_text(prompt_template),
        "attempts": attempts,
        "codex": result_dict(result),
        "infrastructure_failure": result.infrastructure_failure,
        "score": scoring,
    }


def flatten_for_csv(row: dict[str, Any]) -> dict[str, Any]:
    codex = row.get("codex") or {}
    score = row.get("score") or {}
    usage = codex.get("usage") or {}
    return {
        "observation_id": row.get("observation_id"),
        "task_id": row.get("task_id"),
        "task_version": row.get("task_version"),
        "category": row.get("category"),
        "workload": row.get("workload"),
        "tags": ";".join(str(x) for x in row.get("tags", [])),
        "font_id": row.get("font_id"),
        "font_family": row.get("font_family"),
        "font_size_px": row.get("font_size_px"),
        "margin_px": row.get("margin_px"),
        "line_gap_px": row.get("line_gap_px"),
        "width": row.get("width"),
        "height": row.get("height"),
        "patch_columns": row.get("patch_columns"),
        "patch_rows": row.get("patch_rows"),
        "patches": row.get("patches"),
        "estimated_image_tokens": row.get("estimated_image_tokens"),
        "image_sha256": row.get("image_sha256"),
        "font_sha256": row.get("font_sha256"),
        "model": row.get("model"),
        "attempts": row.get("attempts"),
        "thread_id": codex.get("thread_id"),
        "latency_ms": codex.get("latency_ms"),
        "returncode": codex.get("returncode"),
        "infrastructure_failure": row.get("infrastructure_failure"),
        "passed": score.get("passed") if score else None,
        "score": score.get("score") if score else None,
        "response": codex.get("response"),
        "expected_json": json.dumps(row.get("expected"), ensure_ascii=False, sort_keys=True),
        "usage_json": json.dumps(usage, ensure_ascii=False, sort_keys=True),
        "instruction_sha256": row.get("instruction_sha256"),
        "payload_sha256": row.get("payload_sha256"),
        "completed_at": row.get("completed_at"),
    }


def write_results_csv(rows: list[dict[str, Any]], path: Path) -> None:
    flat = [flatten_for_csv(row) for row in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    if not flat:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(flat[0].keys()))
        writer.writeheader()
        writer.writerows(flat)


def summarize_group(items: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [r for r in items if not r.get("infrastructure_failure") and r.get("score")]
    passed = sum(1 for r in valid if bool((r.get("score") or {}).get("passed")))
    total = len(valid)
    low, high = wilson_interval(passed, total)
    patches = [float(r["patches"]) for r in valid if r.get("patches") is not None]
    tokens = [float(r["estimated_image_tokens"]) for r in valid if r.get("estimated_image_tokens") is not None]
    latencies = [float((r.get("codex") or {}).get("latency_ms")) for r in valid if (r.get("codex") or {}).get("latency_ms") is not None]
    accuracy = passed / total if total else 0.0
    mean_tokens = safe_mean(tokens)
    return {
        "observations": len(items),
        "valid": total,
        "infra_failures": len(items) - total,
        "passed": passed,
        "accuracy": accuracy,
        "ci_low": low,
        "ci_high": high,
        "mean_patches": safe_mean(patches),
        "mean_estimated_image_tokens": mean_tokens,
        "accuracy_per_100_image_tokens": (accuracy * 100.0 / mean_tokens) if mean_tokens else 0.0,
        "mean_latency_ms": safe_mean(latencies),
    }


def group_rows(rows: list[dict[str, Any]], keys: tuple[str, ...]) -> list[tuple[tuple[Any, ...], dict[str, Any]]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for row in rows:
        key = tuple(row.get(k) for k in keys)
        groups.setdefault(key, []).append(row)
    return [(key, summarize_group(items)) for key, items in groups.items()]


def markdown_table(headers: list[str], body: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines.extend("| " + " | ".join(row) + " |" for row in body)
    return lines


def pct(value: float) -> str:
    return f"{100.0 * value:.2f}%"


def render_group_section(title: str, rows: list[dict[str, Any]], keys: tuple[str, ...], key_labels: tuple[str, ...]) -> list[str]:
    grouped = group_rows(rows, keys)
    grouped.sort(key=lambda x: tuple(str(v) for v in x[0]))
    body: list[list[str]] = []
    for key, stats in grouped:
        body.append([
            *[str(v) for v in key],
            str(stats["valid"]),
            str(stats["passed"]),
            pct(stats["accuracy"]),
            f"{pct(stats['ci_low'])}–{pct(stats['ci_high'])}",
            f"{stats['mean_patches']:.2f}",
            f"{stats['mean_estimated_image_tokens']:.2f}",
            f"{stats['accuracy_per_100_image_tokens']:.4f}",
            f"{stats['mean_latency_ms']:.0f}",
            str(stats["infra_failures"]),
        ])
    return [
        f"## {title}",
        "",
        *markdown_table(
            [*key_labels, "Valid", "Pass", "Accuracy", "Wilson 95% CI", "Mean patches", "Mean est. image tokens", "Accuracy / 100 image tokens", "Mean latency ms", "Infra failures"],
            body,
        ),
        "",
    ]


def pareto_configs(rows: list[dict[str, Any]]) -> list[tuple[tuple[Any, ...], dict[str, Any]]]:
    configs = group_rows(rows, ("font_id", "font_size_px"))
    valid_configs = [(key, stats) for key, stats in configs if stats["valid"] > 0]
    frontier: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
    for key, stats in valid_configs:
        dominated = False
        for other_key, other in valid_configs:
            if other_key == key:
                continue
            no_worse_tokens = other["mean_estimated_image_tokens"] <= stats["mean_estimated_image_tokens"]
            no_worse_accuracy = other["accuracy"] >= stats["accuracy"]
            strictly_better = (
                other["mean_estimated_image_tokens"] < stats["mean_estimated_image_tokens"]
                or other["accuracy"] > stats["accuracy"]
            )
            if no_worse_tokens and no_worse_accuracy and strictly_better:
                dominated = True
                break
        if not dominated:
            frontier.append((key, stats))
    frontier.sort(key=lambda x: (x[1]["mean_estimated_image_tokens"], -x[1]["accuracy"], str(x[0])))
    return frontier


def write_report(rows: list[dict[str, Any]], path: Path, metadata: dict[str, Any]) -> None:
    overall = summarize_group(rows)
    valid = [r for r in rows if not r.get("infrastructure_failure") and r.get("score")]
    failed_model = [r for r in valid if not bool((r.get("score") or {}).get("passed"))]
    infra = [r for r in rows if r.get("infrastructure_failure")]

    lines = [
        "# Visual Context Efficiency — rendered corpus benchmark report",
        "",
        f"Generated: `{utc_now()}`  ",
        f"Run ID: `{metadata.get('run_id')}`  ",
        f"Model: `{metadata.get('model')}`  ",
        f"Codex CLI: `{metadata.get('codex_version')}`  ",
        f"Prompt template SHA-256: `{metadata.get('prompt_template_sha256')}`",
        "",
        "This report covers the fixed, pre-rendered instruction-image corpus. Each observation was produced by a fresh `codex exec --ephemeral` child session. The source instruction was not supplied as text; only the neutral wrapper, task payload, and corresponding instruction PNG were supplied to the child.",
        "",
        "## Overall",
        "",
        f"- Observations: **{len(rows)}**",
        f"- Valid model observations: **{overall['valid']}**",
        f"- Infrastructure failures: **{overall['infra_failures']}**",
        f"- Passed: **{overall['passed']}**",
        f"- Accuracy: **{pct(overall['accuracy'])}** (Wilson 95% CI {pct(overall['ci_low'])}–{pct(overall['ci_high'])})",
        f"- Mean 32×32 patches: **{overall['mean_patches']:.2f}**",
        f"- Mean estimated Luna image tokens: **{overall['mean_estimated_image_tokens']:.2f}**",
        f"- Mean latency: **{overall['mean_latency_ms']:.0f} ms**",
        "",
    ]

    lines.extend(render_group_section("Coding vs non-coding", rows, ("workload",), ("Workload",)))
    lines.extend(render_group_section("By category", rows, ("category",), ("Category",)))
    lines.extend(render_group_section("By font", rows, ("font_id",), ("Font",)))
    lines.extend(render_group_section("By font size", rows, ("font_size_px",), ("Size px",)))
    lines.extend(render_group_section("By font × size", rows, ("font_id", "font_size_px"), ("Font", "Size px")))

    frontier = pareto_configs(rows)
    lines.extend(["## Empirical font×size Pareto frontier", ""])
    if frontier:
        body = []
        for (font_id, size), stats in frontier:
            body.append([
                str(font_id),
                str(size),
                pct(stats["accuracy"]),
                f"{stats['mean_estimated_image_tokens']:.2f}",
                f"{stats['mean_patches']:.2f}",
                f"{stats['accuracy_per_100_image_tokens']:.4f}",
            ])
        lines.extend(markdown_table(["Font", "Size px", "Accuracy", "Mean est. image tokens", "Mean patches", "Accuracy / 100 image tokens"], body))
    else:
        lines.append("No valid configurations were available.")
    lines.append("")

    task_groups = group_rows(rows, ("task_id", "workload", "category"))
    task_groups.sort(key=lambda x: (x[1]["accuracy"], str(x[0][0])))
    lines.extend(["## Per-task robustness", ""])
    task_body = []
    for (task_id, workload, category), stats in task_groups:
        task_body.append([
            str(task_id), str(workload), str(category), str(stats["valid"]), str(stats["passed"]), pct(stats["accuracy"]), f"{stats['mean_estimated_image_tokens']:.2f}"
        ])
    lines.extend(markdown_table(["Task", "Workload", "Category", "Valid", "Pass", "Accuracy", "Mean est. image tokens"], task_body))
    lines.append("")

    lines.extend(["## Model failures", ""])
    if failed_model:
        lines.append(f"There were **{len(failed_model)}** valid model responses that did not pass their deterministic scorer. The first 100 are listed below.")
        lines.append("")
        failure_body = []
        for row in failed_model[:100]:
            response = str((row.get("codex") or {}).get("response", "")).replace("\n", " ↩ ")
            if len(response) > 120:
                response = response[:117] + "..."
            failure_body.append([
                str(row.get("task_id")), str(row.get("font_id")), str(row.get("font_size_px")), str(row.get("patches")), response
            ])
        lines.extend(markdown_table(["Task", "Font", "Size px", "Patches", "Response"], failure_body))
    else:
        lines.append("No valid model failures were observed.")
    lines.append("")

    lines.extend(["## Infrastructure failures", ""])
    if infra:
        reasons: dict[str, int] = {}
        for row in infra:
            reason = str(row.get("infrastructure_failure"))
            reasons[reason] = reasons.get(reason, 0) + 1
        lines.extend(markdown_table(["Reason", "Count"], [[reason, str(count)] for reason, count in sorted(reasons.items())]))
    else:
        lines.append("No infrastructure failures were observed.")
    lines.append("")

    lines.extend([
        "## Interpretation notes",
        "",
        "- `estimated_image_tokens` uses the configured 1.2-token-per-32×32-patch estimate recorded by the renderer; it is an estimate, not a replacement for any usage fields reported by Codex/OpenAI.",
        "- The Pareto frontier is descriptive for this exact task corpus and run. It treats higher accuracy and lower mean estimated image tokens as better; it is not a statistical equivalence test.",
        "- Coding and non-coding results are shown separately because character-level damage can affect source-code-like instructions differently from redundant natural language.",
        "- Infrastructure failures are excluded from accuracy denominators and retained separately in the raw results.",
        "- `results.csv` is the flattened row-per-image analysis dataset. `results.jsonl` preserves substantially richer Codex event and scoring evidence.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run every pre-rendered benchmark instruction PNG through a fresh Codex child and generate CSV + detailed report."
    )
    parser.add_argument("--manifest", type=Path, default=Path("rendered/all-instructions/manifest.jsonl"))
    parser.add_argument("--tasks", type=Path, default=Path("dataset/tasks.jsonl"))
    parser.add_argument("--model", default="gpt-5.6-luna")
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--infra-retries", type=int, default=1)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--resume", type=Path, help="Existing run directory containing results.jsonl to continue.")
    parser.add_argument("--limit", type=int, help="Run only the first N manifest rows (for smoke testing).")
    parser.add_argument("--prompt-template", default=DEFAULT_PROMPT_TEMPLATE, help="Must contain {payload}; source instruction must not be added as text.")
    parser.add_argument("--dry-run", action="store_true", help="Validate corpus and write metadata without launching Codex.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.model != "gpt-5.6-luna":
        raise SystemExit("this benchmark is currently scoped to gpt-5.6-luna")
    if "{payload}" not in args.prompt_template:
        raise SystemExit("--prompt-template must contain {payload}")
    if args.concurrency < 1:
        raise SystemExit("--concurrency must be at least 1")
    if args.infra_retries < 0:
        raise SystemExit("--infra-retries must be non-negative")

    tasks_list = load_tasks(args.tasks)
    tasks = {task.task_id: task for task in tasks_list}
    manifest = load_manifest(args.manifest)
    if args.limit is not None:
        manifest = manifest[: args.limit]

    expected_ids = {row["task_id"] for row in manifest}
    unknown = expected_ids - tasks.keys()
    if unknown:
        raise SystemExit(f"manifest references unknown task IDs: {', '.join(sorted(unknown))}")

    # Validate every image and its content hash before launching any paid work.
    resolved: list[tuple[dict[str, Any], Path]] = []
    for row in manifest:
        image = resolve_image_path(args.manifest, row)
        digest = hashlib.sha256(image.read_bytes()).hexdigest()
        if digest != row["image_sha256"]:
            raise SystemExit(f"image hash mismatch: {image} expected {row['image_sha256']} got {digest}")
        resolved.append((row, image))

    if args.resume:
        run_dir = args.resume
        run_id = run_dir.name
        if not run_dir.exists():
            raise SystemExit(f"resume directory does not exist: {run_dir}")
    else:
        run_id = make_run_id()
        run_dir = args.output_dir or Path("runs") / run_id
        run_dir.mkdir(parents=True, exist_ok=False)

    raw_path = run_dir / "results.jsonl"
    csv_path = run_dir / "results.csv"
    report_path = run_dir / "REPORT.md"
    metadata_path = run_dir / "run.json"
    completed = load_completed(raw_path)

    version = "dry-run" if args.dry_run else codex_version(args.codex_bin)
    metadata = {
        "run_id": run_id,
        "created_or_resumed_at": utc_now(),
        "model": args.model,
        "codex_version": version,
        "manifest": str(args.manifest),
        "manifest_sha256": hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
        "tasks": str(args.tasks),
        "tasks_sha256": hashlib.sha256(args.tasks.read_bytes()).hexdigest(),
        "prompt_template": args.prompt_template,
        "prompt_template_sha256": sha256_text(args.prompt_template),
        "corpus_observations": len(resolved),
        "concurrency": args.concurrency,
        "timeout_seconds": args.timeout,
        "infra_retries": args.infra_retries,
        "dry_run": args.dry_run,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    pending = [(row, image) for row, image in resolved if make_observation_id(row) not in completed]
    print(f"corpus={len(resolved)} completed={len(completed)} pending={len(pending)} run={run_id}")

    if args.dry_run:
        print(f"validated {len(resolved)} images and hashes; no Codex calls made")
        return

    append_lock = threading.Lock()
    seen_thread_ids: set[str] = {
        str((row.get("codex") or {}).get("thread_id"))
        for row in completed.values()
        if (row.get("codex") or {}).get("thread_id")
    }

    def worker(item: tuple[dict[str, Any], Path]) -> dict[str, Any]:
        row, image = item
        result_row = run_one(
            manifest_row=row,
            image_path=image,
            task=tasks[row["task_id"]],
            model=args.model,
            codex_bin=args.codex_bin,
            timeout=args.timeout,
            infra_retries=args.infra_retries,
            prompt_template=args.prompt_template,
        )
        thread_id = (result_row.get("codex") or {}).get("thread_id")
        with append_lock:
            if thread_id and thread_id in seen_thread_ids:
                result_row["infrastructure_failure"] = "duplicate_thread_id"
                result_row["score"] = None
            if thread_id:
                seen_thread_ids.add(str(thread_id))
            with raw_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(result_row, ensure_ascii=False, sort_keys=True) + "\n")
                f.flush()
        return result_row

    done_count = len(completed)
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = {executor.submit(worker, item): item for item in pending}
        for future in as_completed(futures):
            row = future.result()
            done_count += 1
            score = row.get("score") or {}
            status = "INFRA" if row.get("infrastructure_failure") else ("PASS" if score.get("passed") else "FAIL")
            print(f"[{done_count}/{len(resolved)}] {row['task_id']} {row['font_id']} {row['font_size_px']}px: {status}", flush=True)

    final_by_id = load_completed(raw_path)
    rows = [final_by_id[make_observation_id(row)] for row, _ in resolved if make_observation_id(row) in final_by_id]
    if len(rows) != len(resolved):
        raise SystemExit(f"run incomplete after execution: expected {len(resolved)} observations, found {len(rows)}")

    write_results_csv(rows, csv_path)
    write_report(rows, report_path, metadata)

    overall = summarize_group(rows)
    summary = {
        "run_id": run_id,
        "observations": len(rows),
        **overall,
        "results_csv": str(csv_path),
        "raw_results_jsonl": str(raw_path),
        "report": str(report_path),
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"results CSV: {csv_path}")
    print(f"raw JSONL:   {raw_path}")
    print(f"report:      {report_path}")
    print(f"accuracy:    {overall['passed']}/{overall['valid']} = {overall['accuracy']:.4%}")


if __name__ == "__main__":
    main()
