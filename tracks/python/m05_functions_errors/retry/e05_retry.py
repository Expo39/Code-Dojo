"""Call a function until it works.

Level: medium
Target: 20

Call func() up to `attempts` times and return its result as soon as a call does
not raise.

    If func raises twice and then returns "ok", retry(func, 3) returns "ok" after 3 calls.

Trace by hand (work out the result yourself):

    If func raises once and then returns 42: what does retry(func, 4) return, after how many calls?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify retry
"""


def retry(func, attempts):
    raise NotImplementedError
