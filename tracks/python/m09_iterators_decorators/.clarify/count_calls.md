# count_calls: clarifications

Pattern: decorator

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Positional and keyword arguments are passed through; the return value is returned.
- Each decorated function has its own counter, starting at 0.
