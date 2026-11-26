"""Measure retrieval on its own.

Level: easy
Target: 15

When a RAG answer is wrong, the first question is whether retrieval found the right passage.
Write `retrieval_hit_rate(cases, retrieve, k)`:

- `cases` is a list of dicts with a `question` and `relevant`, a collection of passage ids
  that would answer it.
- `retrieve(question)` returns a list of passage ids, best first.
- A case is a hit when at least one relevant id is among the first `k` ids returned.
- Return a dict: `hits` (a count), `total` (the number of cases), `rate` (hits divided by
  total, or 0.0 with no cases) and `misses` (the questions that were not hits, in order).

    results = {"q1": ["p1", "p2"], "q2": ["p9", "p3"]}
    cases = [{"question": "q1", "relevant": ["p2"]}, {"question": "q2", "relevant": ["p3"]}]
    retrieval_hit_rate(cases, lambda q: results[q], 2)
    -> {"hits": 2, "total": 2, "rate": 1.0, "misses": []}

Trace by hand with a retriever that returns `results[question]` (k = 2):

    results = {"a": ["x", "y", "z"], "b": ["z", "x"], "c": ["y"]}
    cases = [{"question": "a", "relevant": ["z"]}, {"question": "b", "relevant": ["z", "q"]},
             {"question": "c", "relevant": ["x"]}]
    retrieval_hit_rate(cases, lambda q: results[q], 2) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify retrieval_hit_rate
"""


def retrieval_hit_rate(cases, retrieve, k):
    raise NotImplementedError
