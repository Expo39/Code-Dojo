from merge_counts import merge_counts


def test_example():
    assert merge_counts({"x": 1, "y": 2}, {"y": 3, "z": 4}) == {"x": 1, "y": 5, "z": 4}


def test_empty():
    assert merge_counts({}, {}) == {}
    assert merge_counts({"a": 1}, {}) == {"a": 1}


def test_inputs_unchanged():
    a, b = {"k": 1}, {"k": 2}
    merge_counts(a, b)
    assert a == {"k": 1} and b == {"k": 2}
