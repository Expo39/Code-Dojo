# apply_discount: clarifications

Pattern: raise

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Round to 2 decimals.
- Negative price: raise ValueError.
- percent outside 0 to 100: raise ValueError (0 and 100 are allowed).
