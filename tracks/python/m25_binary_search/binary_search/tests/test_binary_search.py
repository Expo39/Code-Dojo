from binary_search import binary_search


def test_found():
    assert binary_search([1, 3, 5, 7, 9], 7) == 3
    assert binary_search([1, 3, 5, 7, 9], 1) == 0
    assert binary_search([1, 3, 5, 7, 9], 9) == 4


def test_missing():
    assert binary_search([1, 3, 5], 4) == -1
    assert binary_search([], 4) == -1


def test_large():
    nums = list(range(0, 2_000_000, 2))
    assert binary_search(nums, 1_234_568) == 617_284
