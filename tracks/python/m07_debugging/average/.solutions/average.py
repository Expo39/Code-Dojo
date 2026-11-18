def average(nums):
    """Return the mean of nums, or None for an empty list."""
    if not nums:
        return None
    total = 0
    for n in nums:
        total += n
    return total / len(nums)
