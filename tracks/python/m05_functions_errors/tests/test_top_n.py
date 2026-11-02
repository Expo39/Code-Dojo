from top_n import top_n


def test_example():
    assert top_n([5, 1, 9, 3], 2) == [9, 5]


def test_key():
    assert top_n(["bb", "a", "ccc"], 1, key=len) == ["ccc"]


def test_n_bounds():
    assert top_n([1, 2], 5) == [2, 1]
    assert top_n([1, 2], 0) == []
