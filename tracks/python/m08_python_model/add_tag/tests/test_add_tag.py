from add_tag import add_tag


def test_fresh_lists():
    assert add_tag("a") == ["a"]
    assert add_tag("b") == ["b"]


def test_given_list():
    assert add_tag("x", ["w"]) == ["w", "x"]
