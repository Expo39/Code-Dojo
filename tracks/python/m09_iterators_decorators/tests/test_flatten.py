from flatten import flatten


def test_example():
    assert flatten([1, [2, [3, 4]], [], 5]) == [1, 2, 3, 4, 5]


def test_flat_and_empty():
    assert flatten([1, 2]) == [1, 2]
    assert flatten([]) == []


def test_deep():
    assert flatten([[[["x"]]]]) == ["x"]
