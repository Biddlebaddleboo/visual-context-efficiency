from vce.scoring import score_response


def test_exact():
    assert score_response("LOW", "LOW", "exact")["passed"]
    assert not score_response("low", "LOW", "exact")["passed"]


def test_casefold_exact():
    assert score_response("Banana", "banana", "casefold_exact")["passed"]


def test_json_exact_ignores_fence():
    result = score_response('```json\n{"city":"Ottawa","country":"Canada"}\n```', {"city": "Ottawa", "country": "Canada"}, "json_exact")
    assert result["passed"]


def test_ordered_lines():
    assert score_response("red\ngreen\nyellow", ["red", "green", "yellow"], "ordered_lines")["passed"]
