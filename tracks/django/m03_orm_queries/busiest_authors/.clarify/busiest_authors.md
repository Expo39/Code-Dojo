# busiest_authors: clarifications

Pattern: annotate-aggregate

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Count novels with a database aggregate over the relation (`annotate` and `Count`), then filter on that count; do not loop over writers in Python.
- Order: count descending, then name ascending.
- `min_novels` of 0 includes writers with no novels (count 0).
- `limit` of 0 or less returns an empty list; do not pass a negative number to a slice.
- The result is a plain `list` of `(name, count)` tuples.
- Exactly one query is expected, and the test counts it.
