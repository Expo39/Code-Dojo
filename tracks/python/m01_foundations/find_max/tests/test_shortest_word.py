from shortest_word import shortest_word


def test_example():
    assert shortest_word(["harbour", "bay", "lighthouse"]) == "bay"


def test_empty():
    assert shortest_word([]) is None


def test_single():
    assert shortest_word(["quay"]) == "quay"


def test_tie_keeps_first():
    assert shortest_word(["pier", "dock", "port"]) == "pier"


def test_shortest_is_last():
    assert shortest_word(["canal", "river", "sea"]) == "sea"
