from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import secrets
import sys

from .codex import codex_version, result_dict, run_fresh
from .dataset import load_tasks
from .render import RenderConfig, render_instruction
from .scoring import score_response


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{secrets.token_hex(4)}"


def _append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, sort_keys=True) + "\n")
        f.flush()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run isolated GPT-5.6 Luna benchmark trials through Codex CLI.")
    parser.add_argument("--tasks", type=Path, default=Path("dataset/tasks.jsonl"))
    parser.add_argument("--condition", choices=["text", "image", "both"], default="both")
    parser.add_argument("--font", default="jetbrains-mono")
    parser.add_argument("--size", type=int, default=14)
    parser.add_argument("--line-gap", type=int, default=1)
    parser.add_argument("--margin", type=int, default=1)
    parser.add_argument("--max-aspect", type=float, default=2.0)
    parser.add_argument("--patch-multiplier", type=float, default=1.2)
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--task-id", action="append", dest="task_ids")
    parser.add_argument("--model", default="gpt-5.6-luna")
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--infra-retries", type=int, default=1)
    parser.add_argument("--runs-dir", type=Path, default=Path("runs"))
    parser.add_argument("--dry-run", action="store_true", help="Render/validate inputs without launching Codex.")
    args = parser.parse_args()

    if args.model != "gpt-5.6-luna":
        parser.error("this benchmark is currently scoped to gpt-5.6-luna")

    tasks = load_tasks(args.tasks)
    if args.task_ids:
        wanted = set(args.task_ids)
        tasks = [task for task in tasks if task.task_id in wanted]
        missing = wanted - {task.task_id for task in tasks}
        if missing:
            parser.error(f"unknown task ids: {', '.join(sorted(missing))}")
    if args.limit is not None:
        tasks = tasks[: args.limit]

    cfg = RenderConfig(
        font_id=args.font,
        font_size_px=args.size,
        line_gap_px=args.line_gap,
        margin_px=args.margin,
        max_aspect_ratio=args.max_aspect,
        patch_token_multiplier=args.patch_multiplier,
    )

    run_id = _run_id()
    run_dir = args.runs_dir / run_id
    image_dir = run_dir / "images"
    results_path = run_dir / "results.jsonl"
    run_dir.mkdir(parents=True, exist_ok=False)

    version = "dry-run"
    if not args.dry_run:
        version = codex_version(args.codex_bin)

    config = {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "codex_version": version,
        "condition": args.condition,
        "repetitions": args.repetitions,
        "render": asdict(cfg),
        "tasks_file": str(args.tasks),
        "task_count": len(tasks),
        "dry_run": args.dry_run,
    }
    (run_dir / "config.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    conditions = [args.condition] if args.condition != "both" else ["text", "image"]
    seen_threads: set[str] = set()
    observations = 0

    for task in tasks:
        rendered = None
        image_path = image_dir / f"{task.task_id}.png"
        if "image" in conditions:
            rendered = render_instruction(task.instruction, image_path, cfg)

        for condition in conditions:
            for repetition in range(1, args.repetitions + 1):
                trial_id = f"{task.task_id}:{condition}:r{repetition}"
                common = {
                    "run_id": run_id,
                    "trial_id": trial_id,
                    "task_id": task.task_id,
                    "task_version": task.version,
                    "category": task.category,
                    "tags": list(task.tags),
                    "condition": condition,
                    "repetition": repetition,
                    "model": args.model,
                    "instruction_sha256": _hash_text(task.instruction),
                    "payload_sha256": _hash_text(task.payload),
                    "scorer": task.scorer,
                    "expected": task.expected,
                    "render": asdict(rendered) if condition == "image" and rendered else None,
                }

                if args.dry_run:
                    _append_jsonl(results_path, {**common, "dry_run": True})
                    observations += 1
                    continue

                if condition == "text":
                    prompt = f"{task.instruction}\n\nTask payload:\n{task.payload}"
                    trial_image = None
                else:
                    prompt = f"Follow the instructions in the attached image.\n\nTask payload:\n{task.payload}"
                    trial_image = image_path

                attempts = 0
                while True:
                    attempts += 1
                    result = run_fresh(
                        prompt,
                        image=trial_image,
                        model=args.model,
                        codex_bin=args.codex_bin,
                        timeout_seconds=args.timeout,
                    )
                    duplicate_thread = bool(result.thread_id and result.thread_id in seen_threads)
                    infra = result.infrastructure_failure
                    if duplicate_thread:
                        infra = "duplicate_thread_id"
                    if result.thread_id:
                        seen_threads.add(result.thread_id)

                    if infra is None or attempts > args.infra_retries:
                        break

                scoring = None if infra else score_response(result.response, task.expected, task.scorer)
                record = {
                    **common,
                    "attempts": attempts,
                    "codex": result_dict(result),
                    "infrastructure_failure": infra,
                    "score": scoring,
                }
                _append_jsonl(results_path, record)
                observations += 1
                status = "INFRA" if infra else ("PASS" if scoring and scoring["passed"] else "FAIL")
                print(f"{trial_id}: {status}")

    print(f"run {run_id}: {observations} observations -> {results_path}")


if __name__ == "__main__":
    main()
