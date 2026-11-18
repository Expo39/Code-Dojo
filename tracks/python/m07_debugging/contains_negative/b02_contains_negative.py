"""Any negative number? (buggy)

Level: tiny
Target: 5

Kind: debug

The function below has ONE bug (sometimes two lines). Do not rewrite it.
1. Read it and predict the bug before running anything. Say it out loud.
2. Run the tests: python dojo.py test contains_negative
3. Confirm with the debugger: a breakpoint (or breakpoint()) and inspect the variables.
4. Fix it with the smallest change and name the bug class.
"""


def contains_negative(nums):
    """Return True if any number is below zero."""
    for n in nums:
        if n < 0:
            return True
        else:
            return False
    return False
