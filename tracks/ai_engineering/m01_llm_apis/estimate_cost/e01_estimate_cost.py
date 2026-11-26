"""What did that model call cost?

Level: easy
Target: 10

A model provider bills every call by tokens, in three kinds, each with its own price in
euros per million tokens: input tokens, output tokens, and cache-read tokens (input the
provider had cached from an earlier call). `input_tokens` does NOT include the cached
ones: they are counted only in `cache_read_tokens`.

`prices` maps a model name to its three prices. Return the cost of one call in euros,
rounded to cents.

    PRICES = {
        "fast-model": {"input": 1.00, "output": 5.00, "cache_read": 0.10},
        "smart-model": {"input": 3.00, "output": 15.00, "cache_read": 0.30},
    }

    estimate_cost("smart-model", 120_000, 8_000, 400_000, PRICES) -> 0.6

Trace by hand (work out the result yourself):

    estimate_cost("fast-model", 500_000, 100_000, 1_000_000, PRICES) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify estimate_cost
"""


def estimate_cost(model, input_tokens, output_tokens, cache_read_tokens, prices):
    raise NotImplementedError
