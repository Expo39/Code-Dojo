from average import average


def test_example():
    assert average([2, 4, 6]) == 4


def test_single():
    assert average([5]) == 5


def test_empty():
    assert average([]) is None
