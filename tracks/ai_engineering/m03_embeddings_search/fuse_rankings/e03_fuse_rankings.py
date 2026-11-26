"""Merge several ranked result lists into one.

Level: medium
Target: 20

Hybrid search runs a keyword search and a vector search and gets two ranked lists of document
ids. A simple way to merge them is reciprocal rank fusion: a document scores
`1 / (k + rank)` in every list that contains it (rank 1 is the first place), and the scores
add up. Write `fuse_rankings(rankings, k=60, top=None)`:

- `rankings` is a list of lists of ids, each best first.
- Return the ids ordered by total score, highest first. Equal scores are ordered by id.
- `top`, when given, limits the result to that many ids.
- An id listed twice in one ranking counts only at its first place there.

    fuse_rankings([["a", "b", "c"], ["b", "c", "d"]]) -> ["b", "c", "a", "d"]

Trace by hand (work out the order yourself):

    fuse_rankings([["x", "y", "z"], ["y", "x"], ["z", "x"]], k=1) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify fuse_rankings
"""


def fuse_rankings(rankings, k=60, top=None):
    raise NotImplementedError
