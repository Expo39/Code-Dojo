"""Top n with an optional key.

Level: easy
Target: 10
Pattern: default-args

Return the n largest items, largest first. `key` is an optional function used
to compare items (like sorted's key). n larger than the list returns all items;
n <= 0 returns [].

    top_n([5, 1, 9, 3], 2) -> [9, 5]
    top_n(["bb", "a", "ccc"], 1, key=len) -> ["ccc"]
"""


def top_n(items, n, key=None):
    raise NotImplementedError
