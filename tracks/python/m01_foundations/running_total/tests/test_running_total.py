from running_total import running_total


def test_example():
    assert running_total([1, 2, 3, 4]) == [1, 3, 6, 10]


def test_empty():
    assert running_total([]) == []


def test_negatives():
    assert running_total([5, -5, 2]) == [5, 0, 2]


def test_input_unchanged():
    nums = [1, 1]
    running_total(nums)
    assert nums == [1, 1]
