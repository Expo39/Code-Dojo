from is_palindrome import is_palindrome


def test_classic():
    assert is_palindrome("A man, a plan, a canal: Panama") is True


def test_not():
    assert is_palindrome("race a car") is False


def test_empty_and_symbols():
    assert is_palindrome("") is True
    assert is_palindrome("?!") is True


def test_digits():
    assert is_palindrome("12 21") is True
    assert is_palindrome("123") is False
