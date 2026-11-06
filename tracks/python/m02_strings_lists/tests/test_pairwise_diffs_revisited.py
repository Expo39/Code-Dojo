from pairwise_diffs_revisited import pairwise_diffs_revisited


def test_example():
    assert pairwise_diffs_revisited([1, 4, 9, 16]) == [3, 5, 7]


def test_short():
    assert pairwise_diffs_revisited([5]) == []
    assert pairwise_diffs_revisited([]) == []


def test_negative_steps():
    assert pairwise_diffs_revisited([10, 7, 7]) == [-3, 0]


def test_returns_new_list():
    nums = [2, 2]
    result = pairwise_diffs_revisited(nums)
    assert result is not nums
    assert nums == [2, 2]
