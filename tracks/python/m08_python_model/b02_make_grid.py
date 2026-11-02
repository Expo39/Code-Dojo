"""Build a grid (buggy).

Level: easy
Target: 10
Pattern: aliasing

Kind: debug

This one is about HOW PYTHON WORKS (names, objects, mutability, scope), not logic.
Predict the bug first, then confirm in the debugger or the Python prompt.
Read first: https://nedbatchelder.com/text/names.html (Facts and myths about Python names and values)
"""


def make_grid(rows, cols, fill=0):
    """Return a rows x cols list of lists, every cell set to fill."""
    return [[fill] * cols] * rows
