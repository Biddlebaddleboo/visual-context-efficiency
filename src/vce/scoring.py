from __future__ import annotations

import json
import re
from typing import Any


def _strip_fence(text: str) -> str:
    value = text.strip()
    if value.startswith("```") and value.endswith("```"):
        lines = value.splitlines()
        if len(lines) >= 3:
            return "\n".join(lines[1:-1]).strip()
    return value


def score_response(response: str, expected: Any, scorer: str) -> dict[str, Any]:
    raw = response.strip()
    if scorer == "exact":
        passed = raw == str(expected)
        return {"passed": passed, "score": 1.0 if passed else 0.0}

    if scorer == "casefold_exact":
        passed = raw.casefold() == str(expected).strip().casefold()
        return {"passed": passed, "score": 1.0 if passed else 0.0}

    if scorer == "normalized_scalar":
        normalize = lambda s: re.sub(r"\s+", " ", str(s).strip()).casefold()
        passed = normalize(raw) == normalize(expected)
        return {"passed": passed, "score": 1.0 if passed else 0.0}

    if scorer == "json_exact":
        try:
            actual = json.loads(_strip_fence(raw))
            passed = actual == expected
            return {"passed": passed, "score": 1.0 if passed else 0.0, "parsed": actual}
        except Exception as exc:
            return {"passed": False, "score": 0.0, "parse_error": str(exc)}

    if scorer == "ordered_lines":
        actual = [line.strip() for line in raw.splitlines() if line.strip()]
        target = [str(x).strip() for x in expected]
        passed = actual == target
        return {"passed": passed, "score": 1.0 if passed else 0.0, "parsed": actual}

    if scorer == "comma_list":
        actual = [part.strip() for part in raw.split(",") if part.strip()]
        target = [str(x).strip() for x in expected]
        passed = actual == target
        return {"passed": passed, "score": 1.0 if passed else 0.0, "parsed": actual}

    raise ValueError(f"unknown scorer: {scorer}")
