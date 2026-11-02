def contains_negative(nums):
    """Return True if any number is below zero."""
    for n in nums:
        if n < 0:
            return True
    return False
