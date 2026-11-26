import pytest
from judge_agreement import judge_agreement


def test_example():
    result = judge_agreement(["pass", "fail", "pass", "fail"], ["pass", "pass", "pass", "fail"])
    assert result == {"agreement": 0.75, "false_pass": 1, "false_fail": 0}


def test_trace():
    result = judge_agreement(["fail", "fail", "pass", "pass", "fail"], ["pass", "fail", "fail", "pass", "pass"])
    assert result["false_pass"] == 2 and result["false_fail"] == 1
    assert abs(result["agreement"] - 0.4) < 1e-9


def test_perfect_agreement():
    assert judge_agreement(["pass", "fail"], ["pass", "fail"]) == {"agreement": 1.0, "false_pass": 0, "false_fail": 0}


def test_total_disagreement():
    result = judge_agreement(["pass", "pass"], ["fail", "fail"])
    assert result == {"agreement": 0.0, "false_pass": 0, "false_fail": 2}


def test_no_outputs():
    assert judge_agreement([], []) == {"agreement": 0.0, "false_pass": 0, "false_fail": 0}


def test_different_lengths_raise():
    with pytest.raises(ValueError):
        judge_agreement(["pass"], ["pass", "fail"])
