from reverse_words import reverse_words


def test_example():
    assert reverse_words("hello big world") == "world big hello"


def test_extra_spaces():
    assert reverse_words("  a   b ") == "b a"


def test_empty():
    assert reverse_words("") == ""
    assert reverse_words("   ") == ""
