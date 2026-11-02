from rank_scores import rank_scores


def test_example():
    assert rank_scores([("bo", 3), ("al", 5), ("cy", 3)]) == [("al", 5), ("bo", 3), ("cy", 3)]


def test_empty():
    assert rank_scores([]) == []


def test_input_unchanged():
    data = [("b", 1), ("a", 2)]
    rank_scores(data)
    assert data == [("b", 1), ("a", 2)]
