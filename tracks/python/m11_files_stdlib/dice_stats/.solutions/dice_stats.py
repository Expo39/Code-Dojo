import random
from collections import Counter


def roll_many(n, sides, rng):
    if n < 0:
        raise ValueError("n must be 0 or more")
    if sides < 1:
        raise ValueError("a die needs at least one side")
    return [rng.randint(1, sides) for _ in range(n)]


def summarise(rolls):
    counts = Counter(rolls)
    return {face: counts[face] for face in sorted(counts)}
