from rotate import rotate


def test_example():
    assert rotate([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]


def test_k_larger():
    assert rotate([1, 2, 3], 4) == [3, 1, 2]


def test_zero_and_full():
    assert rotate([1, 2, 3], 0) == [1, 2, 3]
    assert rotate([1, 2, 3], 3) == [1, 2, 3]


def test_empty():
    assert rotate([], 3) == []


def test_returns_new_list():
    items = [1, 2, 3]
    for k in (0, 3, 1):
        result = rotate(items, k)
        assert result is not items
    assert items == [1, 2, 3]
