# rate_limiter: clarifications

Pattern: class-state-time

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- A call at time t counts against calls made after t - per_seconds: a call exactly per_seconds ago has expired.
- Rejected calls are not recorded.
- Users are independent.
