# squash_repeats: clarifications

Pattern: runs

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Empty list: [].
- A message can come back later after something else: it starts a new run ("a", "a", "b", "a" -> "a (x2)", "b", "a").
- A run at the very end is squashed like any other.
- Messages are compared exactly (case and spaces count).
- Return a new list; `lines` is not changed.
