from count_at_least import count_at_least


def test_example():
    assert count_at_least([10, 25, 30, 5], 25) == 2


def test_empty():
    assert count_at_least([], 3) == 0


def test_equal_counts():
    assert count_at_least([3, 3, 3], 3) == 3


def test_negative_threshold():
    assert count_at_least([-5, -1, 0], -1) == 2
