from common_items import common_items


def test_example():
    assert common_items([3, 1, 2, 2], [2, 3, 4]) == [2, 3]


def test_none_common():
    assert common_items([1], [2]) == []


def test_strings():
    assert common_items(["b", "a"], ["a", "b", "c"]) == ["a", "b"]
