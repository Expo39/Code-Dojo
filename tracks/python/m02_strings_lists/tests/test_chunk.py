import pytest
from chunk import chunk


def test_example():
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_exact():
    assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_empty():
    assert chunk([], 3) == []


def test_bigger_than_list():
    assert chunk([1, 2], 5) == [[1, 2]]


def test_bad_size():
    with pytest.raises(ValueError):
        chunk([1, 2], 0)


def test_size_three():
    assert chunk([1, 2, 3, 4, 5, 6, 7], 3) == [[1, 2, 3], [4, 5, 6], [7]]
