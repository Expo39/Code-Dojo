import pytest
from estimate_cost import estimate_cost

PRICES = {
    "fast-model": {"input": 1.00, "output": 5.00, "cache_read": 0.10},
    "smart-model": {"input": 3.00, "output": 15.00, "cache_read": 0.30},
}


def test_example():
    assert estimate_cost("smart-model", 120_000, 8_000, 400_000, PRICES) == 0.6


def test_cached_tokens_are_cheaper():
    uncached = estimate_cost("fast-model", 2_000_000, 0, 0, PRICES)
    cached = estimate_cost("fast-model", 0, 0, 2_000_000, PRICES)
    assert (uncached, cached) == (2.0, 0.2)


def test_rounded_to_cents():
    assert estimate_cost("fast-model", 4_000, 1_000, 0, PRICES) == 0.01


def test_zero_tokens():
    assert estimate_cost("smart-model", 0, 0, 0, PRICES) == 0


def test_unknown_model_raises():
    with pytest.raises(ValueError):
        estimate_cost("huge-model", 1_000, 1_000, 0, PRICES)


def test_negative_tokens_raise():
    with pytest.raises(ValueError):
        estimate_cost("fast-model", -10, 1_000, 0, PRICES)
