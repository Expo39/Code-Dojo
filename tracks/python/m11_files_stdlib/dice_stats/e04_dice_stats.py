"""Dice rolls you can test.

Level: easy
Target: 15

A board-game helper rolls dice and reports how often each face came up.

Write roll_many(n, sides, rng), which rolls one die with faces 1 to `sides` n times
and returns the rolls as a list. All randomness must come from `rng`, a
random.Random instance passed in by the caller; never call the module-level
random functions. Then write summarise(rolls), which returns a new dict mapping
each face that appeared to how many times it came up, faces in ascending order.

    rolls = roll_many(5, 6, random.Random(7))   -> a list of 5 ints, each 1 to 6
    summarise([3, 1, 3, 6, 1])                  -> {1: 2, 3: 2, 6: 1}

Trace by hand (work out the result yourself):

    summarise([2, 5, 2, 4, 5, 2]) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify dice_stats

Read: https://docs.python.org/3/library/random.html (random.Random, randint)
"""

import random


def roll_many(n, sides, rng):
    raise NotImplementedError


def summarise(rolls):
    raise NotImplementedError
