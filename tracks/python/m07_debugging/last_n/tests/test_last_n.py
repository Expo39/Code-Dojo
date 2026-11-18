from last_n import last_n


def test_example():
    assert last_n([1, 2, 3, 4, 5], 2) == [4, 5]


def test_all():
    assert last_n([1, 2], 5) == [1, 2]


def test_zero():
    assert last_n([1, 2], 0) == []
