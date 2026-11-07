from top_n import top_n


def test_example():
    assert top_n([5, 1, 9, 3], 2) == [9, 5]


def test_key():
    assert top_n(["bb", "a", "ccc"], 1, key=len) == ["ccc"]


def test_n_bounds():
    assert top_n([1, 2], 5) == [2, 1]
    assert top_n([1, 2], 0) == []


def test_type_hints_and_docstring():
    import typing
    hints = typing.get_type_hints(top_n)
    assert {"items", "n", "key", "return"} <= set(hints), "every parameter and the return need a type hint"
    assert hints["n"] is int
    assert type(None) in typing.get_args(hints["key"]), "key can be None, so its hint must allow None"
    assert (top_n.__doc__ or "").strip(), "add a docstring"
