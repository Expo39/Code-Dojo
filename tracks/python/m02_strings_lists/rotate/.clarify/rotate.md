# rotate: clarifications

Pattern: slicing

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- k can be larger than the list: rotate([1, 2, 3], 4) -> [3, 1, 2].
- k = 0 or k = len(items): unchanged.
- Empty list: [].
- Return a new list.
