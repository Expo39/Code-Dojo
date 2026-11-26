from fuse_rankings import fuse_rankings


def test_example():
    assert fuse_rankings([["a", "b", "c"], ["b", "c", "d"]]) == ["b", "c", "a", "d"]


def test_trace_with_small_k():
    # k=1: x = 1/2 + 1/3 + 1/3, y = 1/3 + 1/2, z = 1/4 + 1/2
    assert fuse_rankings([["x", "y", "z"], ["y", "x"], ["z", "x"]], k=1) == ["x", "y", "z"]


def test_equal_scores_ordered_by_id():
    assert fuse_rankings([["p", "q"], ["q", "p"]]) == ["p", "q"]


def test_top_limits_the_result():
    assert fuse_rankings([["a", "b", "c"], ["b", "c", "d"]], top=2) == ["b", "c"]
    assert fuse_rankings([["a"]], top=5) == ["a"]


def test_duplicates_in_one_list_count_once():
    # "a" appears twice in the first list: only its first place counts
    assert fuse_rankings([["a", "b", "a"], ["b"]]) == ["b", "a"]


def test_single_ranking_keeps_its_order():
    assert fuse_rankings([["c", "a", "b"]]) == ["c", "a", "b"]


def test_empty_inputs():
    assert fuse_rankings([]) == []
    assert fuse_rankings([[], []]) == []
