# summarise_scores: clarifications

Pattern: type-hints

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Empty list: every value in the dict is None (the four keys are still there).
- No pass mark: "pass_rate" is None.
- A score exactly equal to the pass mark counts as a pass.
- Duplicate scores all count, in the mean and in the pass rate.
- Do not change the input list.
- Annotations are checked: `scores: list[float]`, `pass_mark: float | None = None`,
  return `dict[str, float | None]`. `typing.Optional[float]` would also be accepted, but use `X | Y`.
- The docstring must be non-empty; what it says is up to you (one line on what the function returns is enough).
