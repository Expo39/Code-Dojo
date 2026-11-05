"""Rate limiter (a classic practical question).

Level: medium
Target: 30

(A classic practical question.)

class RateLimiter(max_calls, per_seconds). allow(user, now) returns True if the
user may make a call at time `now` (in seconds) and records it; otherwise False.
Each user may make at most max_calls calls in any window of per_seconds.

    rl = RateLimiter(2, 10)
    rl.allow("a", 0) -> True;  rl.allow("a", 1) -> True;  rl.allow("a", 2) -> False
    rl.allow("a", 10.5) -> True

Trace by hand (work out the result yourself):

    rl = RateLimiter(3, 5)
    rl.allow("u", 0); rl.allow("u", 2); rl.allow("u", 4); rl.allow("u", 4.5); rl.allow("u", 5.5) -> ? each

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify rate_limiter
"""


class RateLimiter:
    pass
