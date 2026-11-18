from contains_negative import contains_negative


def test_first_negative():
    assert contains_negative([-1, 2]) is True


def test_later_negative():
    assert contains_negative([1, 2, -3]) is True


def test_none():
    assert contains_negative([1, 2]) is False
    assert contains_negative([]) is False
