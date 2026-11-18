from squares_of_evens import squares_of_evens


def test_example():
    assert squares_of_evens([1, 2, 3, 4]) == [4, 16]


def test_negatives_and_zero():
    assert squares_of_evens([-2, 0, 3]) == [4, 0]


def test_empty():
    assert squares_of_evens([]) == []
