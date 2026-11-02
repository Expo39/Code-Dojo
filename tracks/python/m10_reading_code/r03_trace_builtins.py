"""Comprehensions, sorting and generators.

Level: easy
Target: 10
Pattern: tracing

Kind: predict

READ, do not run. For each question, trace the code by hand (write the
variables on paper, step by step) and put your prediction in PREDICTIONS.
Only then run: python dojo.py test trace_builtins
The test checks each prediction against what the code really returns.
Wrong ones: find the exact line where your trace went wrong, and say why.
"""

def q1():
    return {w: len(w) for w in ["hi", "yo", "hey", "hi"]}


def q2():
    people = [("ann", 30), ("bob", 25), ("cat", 30)]
    return [name for name, age in sorted(people, key=lambda p: (-p[1], p[0]))]


def q3():
    gen = (x * x for x in range(4))
    first = sum(gen)
    second = sum(gen)
    return (first, second)


def q4():
    return list(zip("abc", [1, 2]))


def q5():
    return sorted("banana", reverse=True)[:3]


PREDICTIONS = {
    "q1": None,
    "q2": None,
    "q3": None,
    "q4": None,
    "q5": None,
}
