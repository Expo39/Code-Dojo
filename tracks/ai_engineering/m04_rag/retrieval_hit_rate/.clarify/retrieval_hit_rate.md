# retrieval_hit_rate: clarifications

Pattern: hit-at-k

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Only the first `k` ids returned by `retrieve` count; the rest are ignored.
- `relevant` may be a list or a set; one matching id is enough for a hit.
- `k` of 0 or less: no id counts, so every case is a miss.
- No cases: hits 0, total 0, rate 0.0, no misses; do not divide by zero.
- `misses` lists the questions in the order of `cases`.
- Call `retrieve` once per case.
