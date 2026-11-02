"""Position of the first match.

Level: tiny
Target: 5
Pattern: enumerate

Return the index of the first element equal to `target`, or -1 if there is none.
Do not use list.index(): loop with enumerate.

    first_index(["a", "b", "a"], "a") -> 0
    first_index([4, 5, 6], 6) -> 2
    first_index([], 1) -> -1

Think: where does the "not found" return go, inside or after the loop?
"""


def first_index(items, target):
    raise NotImplementedError
