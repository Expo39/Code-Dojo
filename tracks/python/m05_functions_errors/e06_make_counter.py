"""A counter made with a closure.

Level: easy
Target: 10
Pattern: closure

Return a function. Each time it is called it returns the next number, starting
at `start`.

    c = make_counter(5)
    c() -> 5; c() -> 6; c() -> 7

Two counters must not share state. (You will need `nonlocal`.)
"""


def make_counter(start=0):
    raise NotImplementedError
