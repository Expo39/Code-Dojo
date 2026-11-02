from invert_dict import invert_dict


def test_example():
    assert invert_dict({"a": 1, "b": 2, "c": 1}) == {1: ["a", "c"], 2: ["b"]}


def test_empty():
    assert invert_dict({}) == {}


def test_sorted_keys():
    assert invert_dict({"z": 0, "m": 0, "a": 0}) == {0: ["a", "m", "z"]}
