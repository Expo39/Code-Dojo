# chunk: clarifications

Pattern: slicing

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- The last chunk may be shorter.
- Empty list: [].
- size larger than the list: one chunk with everything.
- size less than 1: raise ValueError.
