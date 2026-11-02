"""Rate limiter (a classic practical question).

Level: medium
Target: 30
Pattern: class-state-time

class RateLimiter(max_calls, per_seconds). allow(user, now) returns True if the
user may make a call at time `now` (seconds, a float), and records it; False
otherwise. A user may make at most max_calls calls in any window of
per_seconds: a call at time t counts against calls made after t - per_seconds.
Users are independent.

    rl = RateLimiter(2, 10)
    rl.allow("a", 0) -> True;  rl.allow("a", 1) -> True;  rl.allow("a", 2) -> False
    rl.allow("a", 10.5) -> True   (the call at 0 has expired)
"""


class RateLimiter:
    pass
