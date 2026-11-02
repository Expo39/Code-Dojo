from find_max import find_max


def test_example():
    assert find_max([3, 9, 2]) == 9


def test_all_negative():
    assert find_max([-7, -3, -10]) == -3


def test_empty():
    assert find_max([]) is None


def test_single():
    assert find_max([42]) == 42
