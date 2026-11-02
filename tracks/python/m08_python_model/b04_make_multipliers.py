"""A list of functions (buggy).

Level: medium
Target: 15

Kind: debug

This one is about HOW PYTHON WORKS (names, objects, mutability, scope), not logic.
Predict the bug first, then confirm in the debugger or the Python prompt.
Read first: https://nedbatchelder.com/text/names.html (Facts and myths about Python names and values)
"""


def make_multipliers(n):
    """Return [f0, f1, ..., f(n-1)] where fi(x) == i * x."""
    return [lambda x: i * x for i in range(n)]
