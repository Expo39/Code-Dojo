import pytest
from retry import retry


def flaky(failures):
    state = {"calls": 0}

    def func():
        state["calls"] += 1
        if state["calls"] <= failures:
            raise ConnectionError(f"fail {state['calls']}")
        return "ok"

    return func, state


def test_succeeds_after_failures():
    func, state = flaky(2)
    assert retry(func, 3) == "ok"
    assert state["calls"] == 3


def test_first_try():
    func, state = flaky(0)
    assert retry(func, 5) == "ok"
    assert state["calls"] == 1


def test_gives_up_with_last_error():
    func, state = flaky(10)
    with pytest.raises(ConnectionError, match="fail 3"):
        retry(func, 3)
    assert state["calls"] == 3


def test_bad_attempts():
    func, state = flaky(0)
    with pytest.raises(ValueError):
        retry(func, 0)
    assert state["calls"] == 0
