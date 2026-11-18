from first_repeat import first_repeat


def test_example():
    assert first_repeat([2, 5, 1, 5, 2]) == 5


def test_none():
    assert first_repeat([1, 2, 3]) is None
    assert first_repeat([]) is None


def test_adjacent():
    assert first_repeat(["a", "a"]) == "a"
