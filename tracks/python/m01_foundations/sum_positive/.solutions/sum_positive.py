def sum_positive(nums):
    total = 0
    for n in nums:
        if n > 0:
            total += n
    return total
