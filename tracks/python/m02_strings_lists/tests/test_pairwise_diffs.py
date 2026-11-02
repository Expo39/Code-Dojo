from pairwise_diffs import pairwise_diffs


def test_example():
    assert pairwise_diffs([1, 4, 9, 16]) == [3, 5, 7]


def test_short():
    assert pairwise_diffs([5]) == []
    assert pairwise_diffs([]) == []


def test_negative_steps():
    assert pairwise_diffs([10, 7, 7]) == [-3, 0]
