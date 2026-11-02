"""Tracing loops, ranges and slices.

Level: easy
Target: 10
Pattern: tracing

Kind: predict

READ, do not run. For each question, trace the code by hand (write the
variables on paper, step by step) and put your prediction in PREDICTIONS.
Only then run: python dojo.py test trace_loops
The test checks each prediction against what the code really returns.
Wrong ones: find the exact line where your trace went wrong, and say why.
"""

def q1():
    total = 0
    for i in range(1, 10, 3):
        total += i
    return total


def q2(items):
    return items[1:-1][::-1]


def q3(n):
    result = []
    while n > 1:
        result.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    return result


def q4(words):
    out = {}
    for i, w in enumerate(words):
        out[w[0]] = i
    return out


PREDICTIONS = {
    "q1": None,
    "q2": None,
    "q3": None,
    "q4": None,
}
