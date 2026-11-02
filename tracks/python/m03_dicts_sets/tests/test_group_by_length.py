from group_by_length import group_by_length


def test_example():
    assert group_by_length(["hi", "cat", "yo", "dog"]) == {2: ["hi", "yo"], 3: ["cat", "dog"]}


def test_empty():
    assert group_by_length([]) == {}


def test_duplicates_kept():
    assert group_by_length(["a", "a"]) == {1: ["a", "a"]}
