def count_at_least(nums, threshold):
    count = 0
    for n in nums:
        if n >= threshold:
            count += 1
    return count
