# parse_ints: clarifications

Pattern: try-except

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Spaces around a number are fine: " 2 " -> 2.
- "3.5" is not a whole number: it goes to errors, unchanged.
- Negative numbers are fine.
- Empty list: ([], []).
