"""Decide whether a change may ship.

Level: medium
Target: 20

You run the same evaluation cases before and after a prompt or model change. Each run gives a
dict from case id to True (passed) or False. Write `regression_gate(baseline, candidate,
max_drop)`:

- Compare only the case ids present in both runs. The pass rate of a run is the share of those
  cases it passed. No common cases: raise ValueError.
- `ok` is True when the candidate's rate is at least the baseline's rate minus `max_drop`
  (a fraction, for example 0.02).
- Return a dict: `ok`, `baseline` (its rate), `candidate` (its rate), `regressed` (the sorted
  ids that passed in the baseline and fail in the candidate), `new_cases` (sorted ids only in
  the candidate) and `dropped_cases` (sorted ids only in the baseline).

    regression_gate({"a": True, "b": True, "c": False}, {"a": True, "b": False, "c": True, "d": True}, 0.0)
    -> ok True (both rates are 2/3 on a, b, c), regressed ["b"], new_cases ["d"], dropped_cases []

Trace by hand (all six values):

    regression_gate({"a": True, "b": True, "c": True, "d": False},
                    {"a": True, "b": True, "c": False, "d": True, "e": False}, 0.25) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify regression_gate
"""


def regression_gate(baseline, candidate, max_drop):
    raise NotImplementedError
