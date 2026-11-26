# judge_agreement: clarifications

Pattern: confusion-counts

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Your labels (`human`) are the truth; the judge is what is being checked.
- `false_pass` is the dangerous one: the judge let through something you rejected.
- Only the strings "pass" and "fail" appear.
- No outputs: agreement 0.0 and both counts 0; lists of different lengths raise ValueError.
- `agreement` is a fraction between 0 and 1, not a percentage.
