from sum_positive import sum_positive


def test_example():
    assert sum_positive([3, -1, 4, 0, -5]) == 7


def test_empty():
    assert sum_positive([]) == 0


def test_all_negative():
    assert sum_positive([-2, -3]) == 0


def test_floats():
    assert sum_positive([1.5, -1.0, 2.5]) == 4.0
