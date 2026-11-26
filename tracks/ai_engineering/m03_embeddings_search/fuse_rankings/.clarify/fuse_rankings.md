# fuse_rankings: clarifications

Pattern: rank-fusion

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Rank 1 is the first place in a list; a document's score in a list is 1 / (k + rank).
- Scores from different lists add up; a document missing from a list adds nothing for it.
- Scores that differ by less than 1e-9 are equal; equal scores are ordered by id.
- A repeated id in one list counts once, at its first place (the later copies do not take a rank).
- `top` of None returns every id; a `top` larger than the number of ids returns all of them.
- No rankings, or only empty ones, give an empty list.
