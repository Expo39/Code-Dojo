# days_between: clarifications

Pattern: datetime

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Negative if the second date is earlier.
- Dates are day first: "01/02/2026" is 1 February.
- Invalid dates (e.g. "30/02/2026") raise ValueError: let datetime raise it.
