"""Average of a list (buggy).

Level: tiny
Target: 5
Pattern: accumulator-init

Kind: debug

The function below has ONE bug (sometimes two lines). Do not rewrite it.
1. Read it and predict the bug before running anything. Say it out loud.
2. Run the tests: python dojo.py test average
3. Confirm with the debugger: a breakpoint (or breakpoint()) and inspect the variables.
4. Fix it with the smallest change and name the bug class.
"""


def average(nums):
    """Return the mean of nums, or None for an empty list."""
    if not nums:
        return None
    total = nums[0]
    for n in nums:
        total += n
    return total / len(nums)
