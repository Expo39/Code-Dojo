# regression_gate: clarifications

Pattern: threshold-gate

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Only case ids present in both runs are compared; the others are listed as `new_cases` and `dropped_cases`.
- A rate is passed cases divided by common cases; no common cases raises ValueError.
- `ok` is True when the candidate rate is at least the baseline rate minus `max_drop`; exactly at the limit passes (compare rounded to 9 decimals).
- `regressed` holds only cases that passed before and fail now, sorted; a case that failed before and fails now is not a regression.
- `max_drop` is a fraction (0.02 means 2 percentage points); 0 means no drop allowed.
- Do not change the inputs.
