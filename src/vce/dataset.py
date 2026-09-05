from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class Task:
    task_id: str
    category: str
    instruction: str
    payload: str
    expected: Any
    scorer: str
    tags: tuple[str, ...] = ()
    version: int = 1


def task_from_dict(obj: dict[str, Any]) -> Task:
    return Task(
        task_id=str(obj["task_id"]),
        category=str(obj.get("category", "uncategorized")),
        instruction=str(obj["instruction"]),
        payload=str(obj.get("payload", "")),
        expected=obj.get("expected"),
        scorer=str(obj.get("scorer", "exact")),
        tags=tuple(str(x) for x in obj.get("tags", [])),
        version=int(obj.get("version", 1)),
    )


def load_tasks(path: Path) -> list[Task]:
    tasks: list[Task] = []
    seen: set[str] = set()
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
        task = task_from_dict(obj)
        if task.task_id in seen:
            raise ValueError(f"duplicate task_id {task.task_id!r} at {path}:{line_no}")
        seen.add(task.task_id)
        tasks.append(task)
    if not tasks:
        raise ValueError(f"no tasks found in {path}")
    return tasks


def filter_tasks(tasks: Iterable[Task], ids: set[str] | None = None, limit: int | None = None) -> list[Task]:
    out = [task for task in tasks if not ids or task.task_id in ids]
    if limit is not None:
        out = out[:limit]
    return out
