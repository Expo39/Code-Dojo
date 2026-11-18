import time
import pytest
from timer_block import Timer


def test_measures():
    with Timer() as t:
        time.sleep(0.05)
    assert 0.04 <= t.elapsed < 1


def test_exception_propagates_and_sets_elapsed():
    t = Timer()
    with pytest.raises(KeyError):
        with t:
            raise KeyError("boom")
    assert t.elapsed >= 0
