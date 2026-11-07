import random

import pytest
from dice_stats import roll_many, summarise


def test_same_seed_same_rolls_in_range():
    first = roll_many(50, 6, random.Random(42))
    second = roll_many(50, 6, random.Random(42))
    assert first == second
    assert len(first) == 50
    assert all(isinstance(r, int) and 1 <= r <= 6 for r in first)


def test_uses_passed_rng_not_global():
    random.seed(1)
    a = roll_many(20, 20, random.Random(99))
    random.seed(2)
    b = roll_many(20, 20, random.Random(99))
    assert a == b
    assert all(1 <= r <= 20 for r in a)


def test_summarise_counts_sorted():
    result = summarise([3, 1, 3, 6, 1])
    assert result == {1: 2, 3: 2, 6: 1}
    assert list(result) == [1, 3, 6]


def test_counts_sum_to_n():
    rolls = roll_many(300, 8, random.Random(2026))
    counts = summarise(rolls)
    assert sum(counts.values()) == 300
    assert set(counts) <= set(range(1, 9))
    assert list(counts) == sorted(counts)


def test_zero_rolls():
    assert roll_many(0, 6, random.Random(0)) == []
    assert summarise([]) == {}


def test_invalid_arguments():
    with pytest.raises(ValueError):
        roll_many(-1, 6, random.Random(0))
    with pytest.raises(ValueError):
        roll_many(3, 0, random.Random(0))
