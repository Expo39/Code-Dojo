from odd_floors import odd_floors


def test_example():
    assert odd_floors(7) == [1, 3, 5, 7]


def test_even_top():
    assert odd_floors(10) == [1, 3, 5, 7, 9]


def test_one():
    assert odd_floors(1) == [1]


def test_zero_and_negative():
    assert odd_floors(0) == []
    assert odd_floors(-3) == []
