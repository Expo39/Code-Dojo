"""Quiz score summary, documented and annotated.

Level: easy
Target: 15

Write summarise_scores(scores, pass_mark=None) that returns a dict with the keys
"mean", "best", "worst" and "pass_rate":

- "mean" is the average score rounded to 2 decimals; "best" and "worst" are the
  highest and lowest score.
- "pass_rate" is the share of scores at or above `pass_mark`, rounded to 2 decimals,
  or None when no pass mark is given.

The function must be fully annotated and documented: `scores` is a list of floats,
`pass_mark` is a float or None, the return value is a dict from str to a float or
None (write it with the `X | Y` syntax), and it has a docstring saying what it
returns.

    summarise_scores([6.0, 9.0, 7.5], pass_mark=7.0)
    -> {"mean": 7.5, "best": 9.0, "worst": 6.0, "pass_rate": 0.67}

Trace by hand (work out the result yourself):

    summarise_scores([4.0, 8.0, 5.5, 9.5, 6.0], pass_mark=6.0) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify summarise_scores
"""


def summarise_scores(scores, pass_mark=None):
    raise NotImplementedError
