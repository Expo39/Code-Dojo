"""Check which sources an answer cites.

Level: easy
Target: 15

A RAG answer should cite the passages it used, like `[p2]`, and say "not in the documents"
when the passages do not answer the question. Write `extract_citations(answer, valid_ids)`
that reports what the answer actually did:

- `cited`: the ids in square brackets that are in `valid_ids`, in order of first appearance,
  each once.
- `unknown`: the ids in square brackets that are not in `valid_ids`, same rules. A model
  that invents a source is a failure you want to see.
- `abstained`: True when the answer says "not in the documents" (any capitals).
- An id is letters, digits, `_` or `-` between `[` and `]`; anything else in brackets
  (like `[see below]`) is not a citation.
- Return a dict with those three keys.

    extract_citations("Refunds take 5 days [p2]. Shipping is free [p1][p9].", ["p1", "p2", "p3"])
    -> {"cited": ["p2", "p1"], "unknown": ["p9"], "abstained": False}

Trace by hand (work out all three values):

    extract_citations("Not in the documents [p4] [p1] [p4].", ["p1"]) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify extract_citations
"""

import re


def extract_citations(answer, valid_ids):
    raise NotImplementedError
