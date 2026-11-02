"""A module-level counter (buggy).

Level: easy
Target: 10
Pattern: scope

Kind: debug

This one is about HOW PYTHON WORKS (names, objects, mutability, scope), not logic.
Predict the bug first, then confirm in the debugger or the Python prompt.
Read first: https://nedbatchelder.com/text/names.html (Facts and myths about Python names and values)
"""


total_calls = 0


def record_call():
    """Add one to the module-level total_calls and return the new value."""
    total_calls = total_calls + 1
    return total_calls
