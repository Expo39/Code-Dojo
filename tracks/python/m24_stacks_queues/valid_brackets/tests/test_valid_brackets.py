from valid_brackets import valid_brackets


def test_valid():
    assert valid_brackets("a(b[c]{d})") is True
    assert valid_brackets("") is True


def test_wrong_type():
    assert valid_brackets("(]") is False


def test_unclosed_and_extra_closer():
    assert valid_brackets("((") is False
    assert valid_brackets("())") is False
    assert valid_brackets(")(") is False
