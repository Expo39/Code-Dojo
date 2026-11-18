import pytest
import trace_builtins as m

ACTUAL = {
    "q1": lambda: m.q1(),
    "q2": lambda: m.q2(),
    "q3": lambda: m.q3(),
    "q4": lambda: m.q4(),
    "q5": lambda: m.q5(),
}


@pytest.mark.parametrize("key", list(ACTUAL))
def test_prediction(key):
    assert m.PREDICTIONS[key] is not None, f"{key}: no prediction yet"
    assert m.PREDICTIONS[key] == ACTUAL[key](), f"{key}: trace it again"
