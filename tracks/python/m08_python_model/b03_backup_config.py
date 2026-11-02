"""Copy before changing (buggy).

Level: easy
Target: 10

Kind: debug

This one is about HOW PYTHON WORKS (names, objects, mutability, scope), not logic.
Predict the bug first, then confirm in the debugger or the Python prompt.
Read first: https://nedbatchelder.com/text/names.html (Facts and myths about Python names and values)
"""


def backup_config(config):
    """Return a changed copy of config (a dict of lists) with "debug" appended to
    config["flags"]. The original must not change."""
    new = dict(config)
    new["flags"].append("debug")
    return new
