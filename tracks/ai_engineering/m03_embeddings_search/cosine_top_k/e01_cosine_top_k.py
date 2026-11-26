"""The k closest items to a query.

Level: easy
Target: 15

A search feature stores one embedding (a list of numbers) per document. To answer a query it
embeds the query the same way and returns the documents whose vectors point in the most
similar direction. Write `cosine_top_k(query, items, k)`:

- `query` is a list of numbers; `items` is a list of `(id, vector)` pairs, every vector as
  long as the query.
- The similarity of two vectors is their cosine: the dot product divided by the product of
  their lengths.
- Return the ids of the `k` most similar items, most similar first.

    cosine_top_k([1, 0], [("a", [1, 0]), ("b", [0, 1]), ("c", [1, 1])], 2) -> ["a", "c"]

Trace by hand (work out the order yourself):

    cosine_top_k([0, 2], [("x", [0, 1]), ("y", [3, 4]), ("z", [0, 0]), ("w", [0, 5])], 3) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify cosine_top_k
"""

import math


def cosine_top_k(query, items, k):
    raise NotImplementedError
