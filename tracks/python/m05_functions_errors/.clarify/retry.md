# retry: clarifications

Pattern: higher-order

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Every call raises: re-raise the LAST exception.
- attempts < 1: raise ValueError without calling func.
- Any exception type can occur.
