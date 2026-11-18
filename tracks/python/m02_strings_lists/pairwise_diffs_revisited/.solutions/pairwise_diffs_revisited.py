def pairwise_diffs_revisited(nums):
    return [b - a for a, b in zip(nums, nums[1:])]
