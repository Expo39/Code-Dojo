"""How much can you trust a judge?

Level: easy
Target: 10

An LLM judge grades outputs as "pass" or "fail". Before relying on it, compare it with your
own labels on the same outputs. Write `judge_agreement(human, judge)`:

- `human` and `judge` are lists of `"pass"` or `"fail"`, one per output, in the same order.
- Return a dict: `agreement` (the share of outputs where both agree, or 0.0 for no outputs),
  `false_pass` (the judge said pass, you said fail) and `false_fail` (the judge said fail,
  you said pass).
- Lists of different lengths: raise ValueError.

    judge_agreement(["pass", "fail", "pass", "fail"], ["pass", "pass", "pass", "fail"])
    -> {"agreement": 0.75, "false_pass": 1, "false_fail": 0}

Trace by hand (work out the three values):

    judge_agreement(["fail", "fail", "pass", "pass", "fail"], ["pass", "fail", "fail", "pass", "pass"]) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify judge_agreement
"""


def judge_agreement(human, judge):
    raise NotImplementedError
