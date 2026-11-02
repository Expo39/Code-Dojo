from remove_short import remove_short


def test_adjacent_short_words():
    assert remove_short(["a", "b", "long", "c"], 2) == ["long"]


def test_input_unchanged():
    words = ["a", "abc"]
    remove_short(words, 2)
    assert words == ["a", "abc"]


def test_nothing_removed():
    assert remove_short(["abc"], 1) == ["abc"]
