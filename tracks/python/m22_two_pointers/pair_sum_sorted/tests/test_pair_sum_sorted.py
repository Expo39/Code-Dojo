from pair_sum_sorted import pair_sum_sorted


def test_example():
    assert pair_sum_sorted([1, 3, 4, 6, 9], 10) in [(0, 4), (2, 3)]


def test_none():
    assert pair_sum_sorted([1, 2, 3], 100) is None
    assert pair_sum_sorted([], 1) is None


def test_negatives():
    assert pair_sum_sorted([-5, -1, 2, 8], 3) == (0, 3)


def test_valid_pair():
    nums = [2, 2, 3, 5]
    i, j = pair_sum_sorted(nums, 4)
    assert i < j and nums[i] + nums[j] == 4
