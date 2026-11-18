from first_speeding import first_speeding


def test_example():
    assert first_speeding([30, 45, 55, 40], 50) == 2


def test_first_of_several():
    assert first_speeding([70, 20, 90], 50) == 0


def test_equal_to_limit_is_not_speeding():
    assert first_speeding([50, 50, 51], 50) == 2


def test_none_over():
    assert first_speeding([30, 40], 50) == -1


def test_empty():
    assert first_speeding([], 30) == -1
