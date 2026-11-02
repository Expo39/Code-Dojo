from countdown import countdown


def test_three():
    assert countdown(3) == [3, 2, 1]


def test_one():
    assert countdown(1) == [1]


def test_zero_and_negative():
    assert countdown(0) == []
    assert countdown(-4) == []
