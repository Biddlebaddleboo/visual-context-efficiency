from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from typing import Any


@dataclass(frozen=True)
class CodexResult:
    command: list[str]
    returncode: int
    latency_ms: int
    thread_id: str | None
    response: str
    events: list[dict[str, Any]]
    stderr: str
    usage: dict[str, Any] | None
    infrastructure_failure: str | None


def codex_version(codex_bin: str = "codex") -> str:
    path = shutil.which(codex_bin)
    if not path:
        raise FileNotFoundError(f"Codex CLI not found: {codex_bin}")
    result = subprocess.run([path, "--version"], text=True, capture_output=True, timeout=15)
    return (result.stdout or result.stderr).strip()


def _parse_events(stdout: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for raw in stdout.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            events.append(value)
    return events


def _event_type(event: dict[str, Any]) -> str:
    return str(event.get("type") or event.get("event") or "")


def _extract_thread_id(events: list[dict[str, Any]]) -> str | None:
    for event in events:
        if _event_type(event) == "thread.started":
            for key in ("thread_id", "threadId", "id"):
                value = event.get(key)
                if isinstance(value, str) and value:
                    return value
    return None


def _extract_usage(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    for event in reversed(events):
        if _event_type(event) == "turn.completed" and isinstance(event.get("usage"), dict):
            return event["usage"]
    return None


def run_fresh(
    prompt: str,
    *,
    image: Path | None = None,
    model: str = "gpt-5.6-luna",
    codex_bin: str = "codex",
    timeout_seconds: int = 180,
) -> CodexResult:
    path = shutil.which(codex_bin)
    if not path:
        raise FileNotFoundError(f"Codex CLI not found: {codex_bin}")

    with tempfile.TemporaryDirectory(prefix="vce-codex-") as tmp:
        tmp_path = Path(tmp)
        final_path = tmp_path / "final.txt"
        command = [
            path,
            "exec",
            "--ephemeral",
            "--ignore-user-config",
            "--ignore-rules",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--json",
            "--model",
            model,
            "--output-last-message",
            str(final_path),
            "-C",
            str(tmp_path),
        ]
        # Codex CLI's --image option accepts one or more file arguments and
        # otherwise consumes the trailing prompt as another image path.
        # Put the prompt first so the image attachment cannot swallow it.
        command.append(prompt)
        if image is not None:
            command.extend(["--image", str(image.resolve())])

        started = time.monotonic()
        try:
            completed = subprocess.run(
                command,
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                cwd=tmp_path,
            )
            latency_ms = round((time.monotonic() - started) * 1000)
        except subprocess.TimeoutExpired as exc:
            latency_ms = round((time.monotonic() - started) * 1000)
            return CodexResult(
                command=command,
                returncode=124,
                latency_ms=latency_ms,
                thread_id=None,
                response="",
                events=[],
                stderr=str(exc),
                usage=None,
                infrastructure_failure="timeout",
            )

        events = _parse_events(completed.stdout)
        thread_id = _extract_thread_id(events)
        usage = _extract_usage(events)
        response = final_path.read_text(encoding="utf-8").strip() if final_path.exists() else ""

        failure: str | None = None
        if completed.returncode != 0:
            failure = "codex_nonzero_exit"
        elif not thread_id:
            failure = "fresh_thread_not_verified"
        elif not response:
            failure = "missing_final_response"

        return CodexResult(
            command=command,
            returncode=completed.returncode,
            latency_ms=latency_ms,
            thread_id=thread_id,
            response=response,
            events=events,
            stderr=completed.stderr,
            usage=usage,
            infrastructure_failure=failure,
        )


def result_dict(result: CodexResult) -> dict[str, Any]:
    return asdict(result)
