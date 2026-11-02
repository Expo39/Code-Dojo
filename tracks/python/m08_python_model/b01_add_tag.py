"""Tags with a default list (buggy).

Level: easy
Target: 10

Kind: debug

This one is about HOW PYTHON WORKS (names, objects, mutability, scope), not logic.
Predict the bug first, then confirm in the debugger or the Python prompt.
Read first: https://nedbatchelder.com/text/names.html (Facts and myths about Python names and values)
"""


def add_tag(tag, tags=[]):
    """Return a list of tags with tag added. Without a list, start a new one."""
    tags.append(tag)
    return tags
