from word_lengths_total import word_lengths_total


def test_example():
    assert word_lengths_total(["ab cde", "x"]) == {1: 5, 2: 1}


def test_blank_line():
    assert word_lengths_total([""]) == {1: 0}
