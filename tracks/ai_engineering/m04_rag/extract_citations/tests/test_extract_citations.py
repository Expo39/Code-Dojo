from extract_citations import extract_citations


def test_example():
    result = extract_citations("Refunds take 5 days [p2]. Shipping is free [p1][p9].", ["p1", "p2", "p3"])
    assert result == {"cited": ["p2", "p1"], "unknown": ["p9"], "abstained": False}


def test_abstention_is_found_in_any_capitals_and_other_bracketed_ids_are_unknown():
    result = extract_citations("Not in the documents [p4] [p1] [p4].", ["p1"])
    assert result == {"cited": ["p1"], "unknown": ["p4"], "abstained": True}


def test_each_id_is_reported_once_in_order_of_first_appearance():
    result = extract_citations("[b] then [a] then [b] again and [a]", ["a", "b"])
    assert result["cited"] == ["b", "a"]


def test_brackets_that_are_not_ids_are_ignored():
    result = extract_citations("See [see below] and [p 1] and [] and [p1].", ["p1"])
    assert result == {"cited": ["p1"], "unknown": [], "abstained": False}


def test_no_citations():
    assert extract_citations("Just an answer.", ["p1"]) == {"cited": [], "unknown": [], "abstained": False}


def test_ids_with_digits_underscores_and_dashes():
    result = extract_citations("[doc_1-a] and [DOC_2]", ["doc_1-a"])
    assert result == {"cited": ["doc_1-a"], "unknown": ["DOC_2"], "abstained": False}


def test_empty_answer():
    assert extract_citations("", []) == {"cited": [], "unknown": [], "abstained": False}
