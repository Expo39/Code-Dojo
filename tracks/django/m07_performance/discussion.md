# Discussion questions: m07_performance

Questions for a discussion drill: answer out loud, at your level, with a concrete
example; the tutor follows up (why? when would you not?) and judges against the read-first sources (track
README). No answers here on purpose.

1. A page takes 4 seconds. Walk through how you would find out why before changing anything.
2. What is an N+1 and how do `select_related` and `prefetch_related` each fix it? When can neither be used?
3. What does an index cost, and how do you decide which columns to index?
4. What is a safe cache key and timeout for a dashboard number, and how do you invalidate it?
5. Why do big `OFFSET`s get slow, and what do you do instead?
6. When is a precomputed summary table better than aggregating on demand, and what new problems does it bring?
