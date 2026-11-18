from most_common_char import most_common_char


def test_example():
    assert most_common_char("abracadabra") == "a"


def test_tie_first_wins():
    assert most_common_char("abab") == "a"
    assert most_common_char("bbaa") == "b"


def test_empty():
    assert most_common_char("") is None


def test_later_winner():
    assert most_common_char("abcc") == "c"
