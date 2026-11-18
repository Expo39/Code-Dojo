# format_iban: clarifications

Pattern: slicing

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- The last group may be shorter than `size`.
- Empty code: "".
- `size` larger than the code: the code unchanged, with no spaces.
- `size` less than 1: raise ValueError.
- No trailing space at the end; the code is not validated as a real IBAN.
