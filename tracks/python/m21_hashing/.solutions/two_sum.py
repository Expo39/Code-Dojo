def two_sum(nums, target):
    index_of = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in index_of:
            return [index_of[complement], i]
        index_of[num] = i
    return None
