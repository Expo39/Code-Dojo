"""Call a function until it works.

Level: medium
Target: 20
Pattern: higher-order

Call func() up to `attempts` times. Return its result as soon as a call does
not raise. If every call raises, re-raise the last exception. Raise ValueError
if attempts < 1 (without calling func).

    calls = iter([ValueError, ValueError, "ok"])  # see the tests
"""


def retry(func, attempts):
    raise NotImplementedError
