# days_between: clarifications

Pattern: datetime

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Negative if the second date is earlier.
- Invalid dates (e.g. "2026-02-30") raise ValueError: let datetime raise it.
