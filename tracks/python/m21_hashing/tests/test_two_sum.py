from two_sum import two_sum


def test_example():
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]


def test_duplicates():
    assert two_sum([3, 3], 6) == [0, 1]


def test_later_pair():
    assert two_sum([1, 5, 9, 4], 13) == [2, 3]


def test_none():
    assert two_sum([1, 2], 10) is None
