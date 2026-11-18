from max_window_sum import max_window_sum


def test_example():
    assert max_window_sum([2, 1, 5, 1, 3, 2], 3) == 9


def test_whole_list():
    assert max_window_sum([1, 2], 2) == 3


def test_negatives():
    assert max_window_sum([-3, -1, -2], 1) == -1


def test_bad_k():
    assert max_window_sum([1, 2], 3) is None
    assert max_window_sum([1, 2], 0) is None


def test_large_is_fast():
    nums = list(range(200_000))
    assert max_window_sum(nums, 1000) == sum(nums[-1000:])
