from longest_unique import longest_unique


def test_examples():
    assert longest_unique("abcabcbb") == 3
    assert longest_unique("pwwkew") == 3
    assert longest_unique("bbbb") == 1


def test_empty():
    assert longest_unique("") == 0


def test_tricky_jump():
    assert longest_unique("abba") == 2
    assert longest_unique("dvdf") == 3
