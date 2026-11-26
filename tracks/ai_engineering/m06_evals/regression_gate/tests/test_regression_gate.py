import pytest
from regression_gate import regression_gate


def test_trace():
    baseline = {"a": True, "b": True, "c": True, "d": False}
    candidate = {"a": True, "b": True, "c": False, "d": True, "e": False}
    result = regression_gate(baseline, candidate, 0.25)
    assert result["ok"] is True
    assert abs(result["baseline"] - 0.75) < 1e-9 and abs(result["candidate"] - 0.75) < 1e-9
    assert result["regressed"] == ["c"] and result["new_cases"] == ["e"] and result["dropped_cases"] == []


def test_a_drop_larger_than_allowed_fails_the_gate():
    result = regression_gate({"a": True, "b": True}, {"a": True, "b": False}, 0.25)
    assert result["ok"] is False and result["regressed"] == ["b"]


def test_a_drop_exactly_at_the_limit_passes():
    assert regression_gate({"a": True, "b": True}, {"a": True, "b": False}, 0.5)["ok"] is True


def test_improvement_passes_and_nothing_regressed():
    result = regression_gate({"a": False, "b": True}, {"a": True, "b": True}, 0.0)
    assert result["ok"] is True and result["regressed"] == []
    assert result["baseline"] == 0.5 and result["candidate"] == 1.0


def test_only_common_cases_are_compared_and_the_rest_are_listed():
    baseline = {"a": True, "old1": True, "old2": False}
    candidate = {"a": False, "new1": True}
    result = regression_gate(baseline, candidate, 0.0)
    assert result["baseline"] == 1.0 and result["candidate"] == 0.0
    assert result["dropped_cases"] == ["old1", "old2"] and result["new_cases"] == ["new1"]
    assert result["ok"] is False


def test_regressed_ids_are_sorted():
    baseline = {"z": True, "m": True, "a": True}
    candidate = {"z": False, "m": False, "a": False}
    assert regression_gate(baseline, candidate, 1.0)["regressed"] == ["a", "m", "z"]


def test_no_common_cases_raises():
    with pytest.raises(ValueError):
        regression_gate({"a": True}, {"b": True}, 0.0)
    with pytest.raises(ValueError):
        regression_gate({}, {}, 0.0)
