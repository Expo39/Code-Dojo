from collections import deque


class RateLimiter:
    def __init__(self, max_calls, per_seconds):
        self.max_calls = max_calls
        self.per_seconds = per_seconds
        self._calls = {}

    def allow(self, user, now):
        calls = self._calls.setdefault(user, deque())
        while calls and calls[0] <= now - self.per_seconds:
            calls.popleft()
        if len(calls) >= self.max_calls:
            return False
        calls.append(now)
        return True
