"""The last n items (buggy).

Level: tiny
Target: 5
Pattern: off-by-one

Kind: debug

The function below has ONE bug (sometimes two lines). Do not rewrite it.
1. Read it and predict the bug before running anything. Say it out loud.
2. Run the tests: python dojo.py test last_n
3. Confirm with the debugger: a breakpoint (or breakpoint()) and inspect the variables.
4. Fix it with the smallest change and name the bug class.
"""


def last_n(items, n):
    """Return the last n items (all of them if n >= len). n <= 0 gives []."""
    if n <= 0:
        return []
    start = max(len(items) - n - 1, 0)
    return items[start:]
