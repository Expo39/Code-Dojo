"""Remove duplicates, keep order (buggy).

Level: easy
Target: 10
Pattern: set-order

Kind: debug

The function below has ONE bug (sometimes two lines). Do not rewrite it.
1. Read it and predict the bug before running anything. Say it out loud.
2. Run the tests: python dojo.py test dedupe
3. Confirm with the debugger: a breakpoint (or breakpoint()) and inspect the variables.
4. Fix it with the smallest change and name the bug class.
"""


def dedupe(items):
    """Return items without duplicates, keeping the first occurrence order."""
    return list(set(items))
