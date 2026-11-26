import pytest
from cosine_top_k import cosine_top_k


def test_example():
    items = [("a", [1, 0]), ("b", [0, 1]), ("c", [1, 1])]
    assert cosine_top_k([1, 0], items, 2) == ["a", "c"]


def test_equal_scores_are_ordered_by_id():
    items = [("x", [0, 1]), ("y", [3, 4]), ("z", [0, 0]), ("w", [0, 5])]
    assert cosine_top_k([0, 2], items, 3) == ["w", "x", "y"]


def test_zero_vector_scores_zero_and_does_not_crash():
    items = [("zero", [0, 0]), ("opposite", [-1, 0]), ("same", [1, 0])]
    assert cosine_top_k([1, 0], items, 3) == ["same", "zero", "opposite"]


def test_k_larger_than_items_returns_all():
    assert cosine_top_k([1, 1], [("a", [1, 2]), ("b", [2, 1])], 10) == ["a", "b"]


def test_k_zero_or_negative_returns_empty():
    items = [("a", [1, 0])]
    assert cosine_top_k([1, 0], items, 0) == []
    assert cosine_top_k([1, 0], items, -1) == []


def test_empty_items():
    assert cosine_top_k([1, 0], [], 3) == []


def test_length_of_the_vector_does_not_matter_only_direction():
    items = [("long", [100, 0]), ("diag", [1, 1])]
    assert cosine_top_k([2, 0], items, 1) == ["long"]
