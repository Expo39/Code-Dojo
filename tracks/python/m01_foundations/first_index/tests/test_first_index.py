from first_index import first_index


def test_first_of_duplicates():
    assert first_index(["a", "b", "a"], "a") == 0


def test_last_position():
    assert first_index([4, 5, 6], 6) == 2


def test_missing():
    assert first_index([4, 5, 6], 9) == -1


def test_empty():
    assert first_index([], 1) == -1
