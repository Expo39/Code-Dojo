from dedupe import dedupe


def test_order_kept():
    assert dedupe(["b", "a", "b", "c", "a"]) == ["b", "a", "c"]


def test_numbers():
    assert dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_empty():
    assert dedupe([]) == []
