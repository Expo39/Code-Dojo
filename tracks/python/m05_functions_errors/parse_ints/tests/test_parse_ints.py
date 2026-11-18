from parse_ints import parse_ints


def test_example():
    assert parse_ints(["1", " 2 ", "x", "3.5"]) == ([1, 2], ["x", "3.5"])


def test_negative():
    assert parse_ints(["-4"]) == ([-4], [])


def test_empty():
    assert parse_ints([]) == ([], [])
