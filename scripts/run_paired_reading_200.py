#!/usr/bin/env python3
"""Run the committed Reading-200 image sweep and paired text baseline.

This is intentionally a thin coordinator around the existing fresh-child and
deterministic-scoring helpers. It does not render or modify benchmark images.
"""

from __future__ import annotations

import argparse
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
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
from vce.dataset import Task, load_tasks
from vce.scoring import score_response


IMAGE_PROMPT_TEMPLATE = (
    "Read the passage in the attached image and answer the question below. "
    "Return only the answer, with no explanation.\n\nQuestion:\n{payload}"
)
TEXT_PROMPT_TEMPLATE = (
    "Read the passage below and answer the question. Return only the answer, "
    "with no explanation.\n\nPassage:\n{instruction}\n\nQuestion:\n{payload}"
)
EXPECTED_DATASET_SHA256 = "987988ff39e3ed843ec1b6bb0b6287415c4cbfea83edf6ca4c60a7a25b6f1aef"
EXPECTED_SIZES = (8, 9, 10, 11, 12)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"reading-200-paired-{stamp}-{secrets.token_hex(4)}"


def sha256_bytes(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total <= 0:
        return 0.0, 0.0
    p = successes / total
    z2 = z * z
    denominator = 1.0 + z2 / total
    centre = (p + z2 / (2.0 * total)) / denominator
    margin = z * math.sqrt((p * (1.0 - p) + z2 / 4.0 / total) / total) / denominator
    return max(0.0, centre - margin), min(1.0, centre + margin)


def mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def observation_id(condition: str, task: Task, manifest_row: dict[str, Any] | None = None) -> str:
    if condition == "text":
        return f"{task.task_id}:text:{sha256_text(task.instruction)[:12]}"
    assert manifest_row is not None
    return (
        f"{task.task_id}:fira-sans:{manifest_row['font_size_px']}px:"
        f"{manifest_row['image_sha256'][:12]}"
    )


def load_completed(path: Path) -> dict[str, dict[str, Any]]:
    completed: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return completed
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            row = json.loads(raw)
            if isinstance(row.get("observation_id"), str):
                completed[row["observation_id"]] = row
    return completed


def validate_inputs(tasks_path: Path, manifest_path: Path) -> tuple[list[Task], list[dict[str, Any]], dict[str, Task]]:
    tasks = load_tasks(tasks_path)
    if len(tasks) != 200 or len({task.task_id for task in tasks}) != 200:
        raise SystemExit(f"expected exactly 200 unique tasks, found {len(tasks)}")
    dataset_sha = hashlib.sha256(tasks_path.read_bytes()).hexdigest()
    if dataset_sha != EXPECTED_DATASET_SHA256:
        raise SystemExit(
            f"dataset SHA mismatch: expected {EXPECTED_DATASET_SHA256}, got {dataset_sha}"
        )

    rows = [json.loads(raw) for raw in manifest_path.read_text(encoding="utf-8").splitlines() if raw.strip()]
    if len(rows) != 1000:
        raise SystemExit(f"expected exactly 1,000 manifest rows, found {len(rows)}")
    task_map = {task.task_id: task for task in tasks}
    counts: dict[int, int] = {size: 0 for size in EXPECTED_SIZES}
    ids: set[str] = set()
    paths: set[str] = set()
    for row in rows:
        if row.get("font_id") != "fira-sans":
            raise SystemExit(f"unexpected font: {row.get('font_id')}")
        size = int(row.get("font_size_px", -1))
        if size not in counts:
            raise SystemExit(f"unexpected font size: {size}")
        if row.get("task_id") not in task_map:
            raise SystemExit(f"manifest references unknown task: {row.get('task_id')}")
        counts[size] += 1
        current_id = observation_id("image", task_map[row["task_id"]], row)
        if current_id in ids:
            raise SystemExit(f"duplicate image observation ID: {current_id}")
        ids.add(current_id)
        path = Path(str(row["path"]))
        if path.is_absolute():
            resolved = path
        else:
            resolved = Path.cwd() / path
        if not resolved.exists():
            raise SystemExit(f"missing image: {resolved}")
        if sha256_bytes(resolved) != row["image_sha256"]:
            raise SystemExit(f"image hash mismatch: {resolved}")
        paths.add(str(resolved.resolve()))
    if counts != {size: 200 for size in EXPECTED_SIZES}:
        raise SystemExit(f"unexpected rows per size: {counts}")
    actual_pngs = {str(path.resolve()) for path in (manifest_path.parent).rglob("*.png")}
    if actual_pngs != paths or len(actual_pngs) != 1000:
        raise SystemExit("manifest/image PNG set mismatch")
    return tasks, rows, task_map


def stats(rows: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [row for row in rows if not row.get("infrastructure_failure") and row.get("score")]
    passed = sum(bool(row["score"].get("passed")) for row in valid)
    low, high = wilson_interval(passed, len(valid))
    patches = [float(row["patches"]) for row in valid if row.get("patches") is not None]
    image_tokens = [float(row["estimated_image_tokens"]) for row in valid if row.get("estimated_image_tokens") is not None]
    latency = [float(row["codex"].get("latency_ms")) for row in valid if row.get("codex", {}).get("latency_ms") is not None]
    text_tokens = [float(row["text_input_tokens"]) for row in valid if row.get("text_input_tokens") is not None]
    accuracy = passed / len(valid) if valid else 0.0
    return {
        "observations": len(rows),
        "valid": len(valid),
        "infrastructure_failures": len(rows) - len(valid),
        "passed": passed,
        "accuracy": accuracy,
        "ci_low": low,
        "ci_high": high,
        "mean_patches": mean(patches),
        "mean_estimated_image_tokens": mean(image_tokens),
        "mean_latency_ms": mean(latency),
        "text_input_tokens_available": len(text_tokens),
        "mean_text_input_tokens": mean(text_tokens),
        "min_text_input_tokens": min(text_tokens) if text_tokens else None,
        "max_text_input_tokens": max(text_tokens) if text_tokens else None,
    }


def pct(value: float) -> str:
    return f"{100.0 * value:.2f}%"


def md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def group_stats(rows: list[dict[str, Any]], key: str, values: list[Any]) -> dict[Any, dict[str, Any]]:
    return {value: stats([row for row in rows if row.get(key) == value]) for value in values}


def write_report(rows: list[dict[str, Any]], path: Path, metadata: dict[str, Any]) -> dict[str, Any]:
    text_rows = [row for row in rows if row["condition"] == "text"]
    image_rows = [row for row in rows if row["condition"] == "image"]
    baseline = stats(text_rows)
    by_size = group_stats(image_rows, "font_size_px", list(EXPECTED_SIZES))
    by_category_text = {category: stats([row for row in text_rows if row["category"] == category]) for category in sorted({row["category"] for row in text_rows})}
    by_category_size = {
        size: {category: stats([row for row in image_rows if row["font_size_px"] == size and row["category"] == category]) for category in sorted({row["category"] for row in image_rows})}
        for size in EXPECTED_SIZES
    }

    points = [(size, by_size[size]) for size in EXPECTED_SIZES]
    frontier: list[tuple[int, dict[str, Any]]] = []
    for size, point in points:
        dominated = any(
            other_size != size
            and other["accuracy"] >= point["accuracy"]
            and other["mean_estimated_image_tokens"] <= point["mean_estimated_image_tokens"]
            and (
                other["accuracy"] > point["accuracy"]
                or other["mean_estimated_image_tokens"] < point["mean_estimated_image_tokens"]
            )
            for other_size, other in points
        )
        if not dominated:
            frontier.append((size, point))
    frontier.sort(key=lambda item: (item[1]["mean_estimated_image_tokens"], -item[1]["accuracy"]))
    closest_size = min(EXPECTED_SIZES, key=lambda size: abs(by_size[size]["accuracy"] - baseline["accuracy"]))

    task_by_size = {
        size: {row["task_id"]: row for row in image_rows if row["font_size_px"] == size}
        for size in EXPECTED_SIZES
    }
    task_ids = sorted(task_by_size[8])
    recoveries = []
    for task_id in task_ids:
        low = bool(task_by_size[8][task_id].get("score", {}).get("passed"))
        high = bool(task_by_size[12][task_id].get("score", {}).get("passed"))
        recoveries.append((task_id, task_by_size[8][task_id]["category"], low, high))
    recovery_counts = {
        "8_pass_12_pass": sum(low and high for _, _, low, high in recoveries),
        "8_fail_12_recovered": sum(not low and high for _, _, low, high in recoveries),
        "8_pass_12_regressed": sum(low and not high for _, _, low, high in recoveries),
        "8_fail_12_fail": sum(not low and not high for _, _, low, high in recoveries),
    }
    infrastructure = [row for row in rows if row.get("infrastructure_failure")]
    retry_rows = [row for row in rows if int(row.get("attempts", 1)) > 1]
    overall_valid = sum(1 for row in rows if not row.get("infrastructure_failure") and row.get("score"))

    summary = {
        "run_id": metadata["run_id"],
        "observations": len(rows),
        "valid": overall_valid,
        "infrastructure_failures": len(infrastructure),
        "text_baseline": baseline,
        "image_by_size": {str(size): by_size[size] for size in EXPECTED_SIZES},
        "category_text": by_category_text,
        "category_by_size": {str(size): by_category_size[size] for size in EXPECTED_SIZES},
        "recovery_8_to_12": recovery_counts,
        "pareto_frontier": [{"size_px": size, **point} for size, point in frontier],
        "closest_size_to_text_accuracy": closest_size,
        "infrastructure_retry_rows": len(retry_rows),
        "results_csv": str(path.with_name("results.csv")),
        "raw_results_jsonl": str(path.with_name("results.jsonl")),
        "report": str(path),
    }

    lines = [
        "# Reading-200 paired text/image benchmark report",
        "",
        f"Generated: `{utc_now()}`  ",
        f"Run ID: `{metadata['run_id']}`  ",
        f"Model: `{metadata['model']}`  ",
        f"Codex CLI: `{metadata['codex_version']}`  ",
        f"Dataset SHA-256: `{metadata['dataset_sha256']}`  ",
        f"Image manifest SHA-256: `{metadata['manifest_sha256']}`",
        "",
        "The dataset and PNG corpus are immutable committed inputs. Every observation used a fresh `codex exec --ephemeral` child session. Image observations supplied the passage only through the assigned PNG; text observations supplied the original passage as text. No text/image equivalence claim is made beyond these paired results.",
        "",
        "## Completion and isolation",
        "",
        f"- Total observations: **{len(rows)}** ({metadata['image_observations']} image + {metadata['text_observations']} text)",
        f"- Valid scored observations: **{overall_valid}**",
        f"- Final infrastructure failures: **{len(infrastructure)}**",
        f"- Rows with infrastructure retries: **{len(retry_rows)}**",
        f"- Unique child thread IDs: **{len({row.get('codex', {}).get('thread_id') for row in rows if row.get('codex', {}).get('thread_id')})}**",
        "",
        "## Plain-text baseline",
        "",
        f"- Accuracy: **{baseline['passed']}/{baseline['valid']} = {pct(baseline['accuracy'])}** (Wilson 95% CI {pct(baseline['ci_low'])}–{pct(baseline['ci_high'])})",
        f"- Mean latency: **{baseline['mean_latency_ms']:.0f} ms**",
        f"- Observed Codex input tokens: **{baseline['mean_text_input_tokens']:.2f} mean** ({baseline['min_text_input_tokens']:.0f}–{baseline['max_text_input_tokens']:.0f}, n={baseline['text_input_tokens_available']})" if baseline["text_input_tokens_available"] else "- Observed Codex input tokens: unavailable",
        "",
        "## Image results by size",
        "",
    ]
    image_table = []
    for size in EXPECTED_SIZES:
        item = by_size[size]
        gap = item["accuracy"] - baseline["accuracy"]
        image_table.append([
            f"{size}px", f"{item['passed']}/{item['valid']}", pct(item["accuracy"]),
            f"{pct(item['ci_low'])}–{pct(item['ci_high'])}", f"{gap:+.2%}",
            f"{item['mean_patches']:.2f}", f"{item['mean_estimated_image_tokens']:.2f}", f"{item['mean_latency_ms']:.0f}",
        ])
    lines.extend(md_table(["Size", "Passed/valid", "Accuracy", "Wilson 95% CI", "Gap vs text", "Mean patches", "Mean est. image tokens", "Mean latency ms"], image_table))
    lines.extend(["", f"Smallest size closest to text-baseline accuracy: **{closest_size}px** (absolute gap {abs(by_size[closest_size]['accuracy'] - baseline['accuracy']):.2%}).", ""])

    lines.extend(["## Category accuracy", "", "Text baseline:", ""])
    category_names = sorted(by_category_text)
    text_category_table = []
    for category in category_names:
        item = by_category_text[category]
        text_category_table.append([category, f"{item['passed']}/{item['valid']}", pct(item['accuracy']), f"{pct(item['ci_low'])}–{pct(item['ci_high'])}"])
    lines.extend(md_table(["Category", "Passed/valid", "Accuracy", "Wilson 95% CI"], text_category_table))
    lines.extend(["", "Image conditions:", ""])
    category_table = []
    for category in category_names:
        for size in EXPECTED_SIZES:
            item = by_category_size[size][category]
            category_table.append([f"{size}px", category, f"{item['passed']}/{item['valid']}", pct(item['accuracy']), f"{pct(item['ci_low'])}–{pct(item['ci_high'])}"])
    lines.extend(md_table(["Size", "Category", "Passed/valid", "Accuracy", "Wilson 95% CI"], category_table))
    lines.extend(["", "Cause/location recovery from 8px to 12px:", ""])
    cause_location = []
    for category in ("reading_cause", "reading_location"):
        if category not in by_category_size[8] or category not in by_category_size[12]:
            continue
        low = by_category_size[8][category]["accuracy"]
        high = by_category_size[12][category]["accuracy"]
        cause_location.append([category, pct(low), pct(high), f"{high - low:+.2%}"])
    if cause_location:
        lines.extend(md_table(["Category", "8px", "12px", "Change"], cause_location))
    else:
        lines.append("Cause/location categories are not represented in this smoke subset.")

    lines.extend(["", "## Task-by-task recovery from 8px to 12px", ""])
    lines.append(f"Recovered (8px fail → 12px pass): **{recovery_counts['8_fail_12_recovered']}**; regressed: **{recovery_counts['8_pass_12_regressed']}**; stable pass: **{recovery_counts['8_pass_12_pass']}**; stable fail: **{recovery_counts['8_fail_12_fail']}**.")
    lines.append("")
    recovery_table = []
    for task_id, category, low, high in recoveries:
        recovery_table.append([task_id, category, "PASS" if low else "FAIL", "PASS" if high else "FAIL", f"{int(high) - int(low):+d}"])
    lines.extend(md_table(["Task", "Category", "8px", "12px", "Delta"], recovery_table))

    lines.extend(["", "## Accuracy-vs-image-token Pareto frontier", ""])
    frontier_table = []
    for size, item in frontier:
        frontier_table.append([f"{size}px", pct(item["accuracy"]), f"{item['mean_estimated_image_tokens']:.2f}", f"{item['mean_patches']:.2f}"])
    lines.extend(md_table(["Size", "Accuracy", "Mean est. image tokens", "Mean patches"], frontier_table))

    lines.extend(["", "## Infrastructure failures and retries", ""])
    if infrastructure:
        reasons: dict[str, int] = {}
        for row in infrastructure:
            reason = str(row.get("infrastructure_failure"))
            reasons[reason] = reasons.get(reason, 0) + 1
        lines.extend(md_table(["Reason", "Count"], [[reason, str(count)] for reason, count in sorted(reasons.items())]))
    else:
        lines.append("No final infrastructure failures were observed.")
    if retry_rows:
        lines.append("")
        lines.append("Infrastructure-retry rows are retained with their attempt count; valid model responses, including valid wrong answers, were not retried.")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def flatten(row: dict[str, Any]) -> dict[str, Any]:
    codex = row.get("codex") or {}
    score = row.get("score") or {}
    usage = codex.get("usage") or {}
    return {
        "observation_id": row.get("observation_id"),
        "condition": row.get("condition"),
        "task_id": row.get("task_id"),
        "category": row.get("category"),
        "font_id": row.get("font_id"),
        "font_size_px": row.get("font_size_px"),
        "patches": row.get("patches"),
        "estimated_image_tokens": row.get("estimated_image_tokens"),
        "image_sha256": row.get("image_sha256"),
        "image_path": row.get("image_path"),
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
        "text_input_tokens": row.get("text_input_tokens"),
        "instruction_sha256": row.get("instruction_sha256"),
        "payload_sha256": row.get("payload_sha256"),
        "prompt_template_sha256": row.get("prompt_template_sha256"),
        "completed_at": row.get("completed_at"),
    }


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    flattened = [flatten(row) for row in rows]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(flattened[0]))
        writer.writeheader()
        writer.writerows(flattened)


def run_observation(
    item: dict[str, Any],
    *,
    model: str,
    codex_bin: str,
    timeout: int,
    infra_retries: int,
) -> dict[str, Any]:
    task: Task = item["task"]
    condition = item["condition"]
    if condition == "image":
        prompt_template = IMAGE_PROMPT_TEMPLATE
        prompt = prompt_template.format(payload=task.payload)
        image_path = item["image_path"]
    else:
        prompt_template = TEXT_PROMPT_TEMPLATE
        prompt = prompt_template.format(instruction=task.instruction, payload=task.payload)
        image_path = None

    attempts = 0
    result = None
    while attempts <= infra_retries:
        attempts += 1
        result = run_fresh(prompt, image=image_path, model=model, codex_bin=codex_bin, timeout_seconds=timeout)
        if result.infrastructure_failure is None:
            break
    assert result is not None
    score = None if result.infrastructure_failure else score_response(result.response, task.expected, task.scorer)
    usage = result.usage or {}
    return {
        "observation_id": item["observation_id"],
        "completed_at": utc_now(),
        "condition": condition,
        "task_id": task.task_id,
        "task_version": task.version,
        "category": task.category,
        "tags": list(task.tags),
        "workload": "coding" if "coding" in {tag.casefold() for tag in task.tags} else "noncoding",
        "instruction_sha256": sha256_text(task.instruction),
        "payload_sha256": sha256_text(task.payload),
        "expected": task.expected,
        "scorer": task.scorer,
        "font_id": item.get("font_id"),
        "font_family": item.get("font_family"),
        "font_size_px": item.get("font_size_px"),
        "width": item.get("width"),
        "height": item.get("height"),
        "patch_columns": item.get("patch_columns"),
        "patch_rows": item.get("patch_rows"),
        "patches": item.get("patches"),
        "estimated_image_tokens": item.get("estimated_image_tokens"),
        "font_sha256": item.get("font_sha256"),
        "image_sha256": item.get("image_sha256"),
        "image_path": str(image_path) if image_path else None,
        "model": model,
        "prompt_template_sha256": sha256_text(prompt_template),
        "text_input_tokens": usage.get("input_tokens") if condition == "text" else None,
        "attempts": attempts,
        "codex": result_dict(result),
        "infrastructure_failure": result.infrastructure_failure,
        "score": score,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the paired Reading-200 image sweep and text baseline.")
    parser.add_argument("--tasks", type=Path, default=Path("dataset/reading_200.jsonl"))
    parser.add_argument("--manifest", type=Path, default=Path("rendered/reading-200/manifest.jsonl"))
    parser.add_argument("--model", default="gpt-5.6-luna")
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--infra-retries", type=int, default=1)
    parser.add_argument("--runs-root", type=Path, default=Path("runs"))
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--limit", type=int, help="Smoke-test task count per condition (omit for full run).")
    args = parser.parse_args()
    if args.model != "gpt-5.6-luna":
        parser.error("this benchmark is scoped to gpt-5.6-luna")
    if args.concurrency < 1 or args.timeout <= 0 or args.infra_retries < 0:
        parser.error("concurrency, timeout, and infra-retries must be positive/non-negative")

    tasks, manifest, task_map = validate_inputs(args.tasks, args.manifest)
    manifest_by_task_size = {(row["task_id"], int(row["font_size_px"])): row for row in manifest}
    ordered_tasks = tasks[: args.limit] if args.limit is not None else tasks
    if not ordered_tasks:
        parser.error("--limit must select at least one task")

    items: list[dict[str, Any]] = []
    for size in EXPECTED_SIZES:
        for task in ordered_tasks:
            row = manifest_by_task_size[(task.task_id, size)]
            image_path = (Path.cwd() / row["path"]).resolve()
            items.append({"condition": "image", "task": task, "observation_id": observation_id("image", task, row), "image_path": image_path, **row})
    for task in ordered_tasks:
        items.append({"condition": "text", "task": task, "observation_id": observation_id("text", task), "image_path": None})
    expected_ids = [item["observation_id"] for item in items]
    if len(set(expected_ids)) != len(expected_ids):
        raise SystemExit("duplicate paired observation IDs")

    if args.resume:
        run_dir = args.resume
        if not run_dir.exists():
            raise SystemExit(f"resume directory does not exist: {run_dir}")
        existing_metadata_path = run_dir / "run.json"
        existing_metadata = json.loads(existing_metadata_path.read_text(encoding="utf-8")) if existing_metadata_path.exists() else {}
        run_id = str(existing_metadata.get("run_id") or run_dir.name)
    else:
        run_id = make_run_id()
        run_dir = args.output_dir or (args.runs_root / datetime.now(timezone.utc).strftime("%Y-%m-%d") / datetime.now(timezone.utc).strftime("%H-%M-%S.%fZ"))
        run_dir.mkdir(parents=True, exist_ok=False)

    raw_path = run_dir / "results.jsonl"
    completed = load_completed(raw_path)
    metadata = {
        "run_id": run_id,
        "created_or_resumed_at": utc_now(),
        "model": args.model,
        "codex_version": codex_version(args.codex_bin),
        "tasks": str(args.tasks),
        "dataset_sha256": hashlib.sha256(args.tasks.read_bytes()).hexdigest(),
        "manifest": str(args.manifest),
        "manifest_sha256": hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
        "image_prompt_template": IMAGE_PROMPT_TEMPLATE,
        "image_prompt_template_sha256": sha256_text(IMAGE_PROMPT_TEMPLATE),
        "text_prompt_template": TEXT_PROMPT_TEMPLATE,
        "text_prompt_template_sha256": sha256_text(TEXT_PROMPT_TEMPLATE),
        "task_count": len(ordered_tasks),
        "image_observations": len(ordered_tasks) * len(EXPECTED_SIZES),
        "text_observations": len(ordered_tasks),
        "corpus_observations": len(items),
        "concurrency": args.concurrency,
        "timeout_seconds": args.timeout,
        "infra_retries": args.infra_retries,
        "smoke_limit": args.limit,
    }
    (run_dir / "run.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    pending = [item for item in items if item["observation_id"] not in completed or completed[item["observation_id"]].get("infrastructure_failure")]
    print(f"corpus={len(items)} completed={len(items)-len(pending)} pending={len(pending)} run={run_id}", flush=True)
    append_lock = threading.Lock()
    seen_threads = {str(row.get("codex", {}).get("thread_id")) for row in completed.values() if row.get("codex", {}).get("thread_id")}

    def worker(item: dict[str, Any]) -> dict[str, Any]:
        result = run_observation(item, model=args.model, codex_bin=args.codex_bin, timeout=args.timeout, infra_retries=args.infra_retries)
        with append_lock:
            thread_id = result.get("codex", {}).get("thread_id")
            if thread_id and thread_id in seen_threads:
                result["infrastructure_failure"] = "duplicate_thread_id"
                result["score"] = None
            if thread_id:
                seen_threads.add(str(thread_id))
            with raw_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")
                handle.flush()
        return result

    done = len(items) - len(pending)
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = {executor.submit(worker, item): item for item in pending}
        for future in as_completed(futures):
            result = future.result()
            done += 1
            score = result.get("score") or {}
            status = "INFRA" if result.get("infrastructure_failure") else ("PASS" if score.get("passed") else "FAIL")
            print(f"[{done}/{len(items)}] {result['condition']} {result['task_id']} {result.get('font_size_px') or '-'}: {status}", flush=True)

    final = load_completed(raw_path)
    if set(final) != set(expected_ids):
        missing = sorted(set(expected_ids) - set(final))
        raise SystemExit(f"run incomplete: missing {len(missing)} observations")
    rows = [final[identifier] for identifier in expected_ids]
    write_csv(rows, run_dir / "results.csv")
    summary = write_report(rows, run_dir / "REPORT.md", metadata)
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"results CSV: {run_dir / 'results.csv'}")
    print(f"raw JSONL:   {raw_path}")
    print(f"report:      {run_dir / 'REPORT.md'}")
    print(f"text accuracy: {summary['text_baseline']['passed']}/{summary['text_baseline']['valid']} = {summary['text_baseline']['accuracy']:.4%}")
    for size in EXPECTED_SIZES:
        item = summary["image_by_size"][str(size)]
        print(f"image {size}px accuracy: {item['passed']}/{item['valid']} = {item['accuracy']:.4%}")


if __name__ == "__main__":
    main()
