from count_long_words import count_long_words


def test_example():
    assert count_long_words(["fjord", "ash", "glacier", "elm"], 5) == 2


def test_empty():
    assert count_long_words([], 3) == 0


def test_exact_length_counts():
    assert count_long_words(["oak", "elm", "ash"], 3) == 3


def test_none_long_enough():
    assert count_long_words(["a", "be", "sea"], 4) == 0


def test_zero_minimum_counts_everything():
    assert count_long_words(["", "x", "tree"], 0) == 3
