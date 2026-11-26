from retrieval_hit_rate import retrieval_hit_rate

RESULTS = {"a": ["x", "y", "z"], "b": ["z", "x"], "c": ["y"]}


def retrieve(question):
    return RESULTS[question]


def test_trace_example():
    cases = [{"question": "a", "relevant": ["z"]}, {"question": "b", "relevant": ["z", "q"]},
             {"question": "c", "relevant": ["x"]}]
    result = retrieval_hit_rate(cases, retrieve, 2)
    assert result["hits"] == 1 and result["total"] == 3 and result["misses"] == ["a", "c"]
    assert abs(result["rate"] - 1 / 3) < 1e-9


def test_k_decides_what_counts():
    cases = [{"question": "a", "relevant": ["z"]}]
    assert retrieval_hit_rate(cases, retrieve, 2)["hits"] == 0
    assert retrieval_hit_rate(cases, retrieve, 3)["hits"] == 1


def test_any_relevant_id_is_enough_and_relevant_can_be_a_set():
    cases = [{"question": "b", "relevant": {"q", "x"}}]
    assert retrieval_hit_rate(cases, retrieve, 2)["rate"] == 1.0


def test_no_cases():
    assert retrieval_hit_rate([], retrieve, 3) == {"hits": 0, "total": 0, "rate": 0.0, "misses": []}


def test_k_zero_hits_nothing():
    cases = [{"question": "a", "relevant": ["x"]}]
    result = retrieval_hit_rate(cases, retrieve, 0)
    assert result["hits"] == 0 and result["misses"] == ["a"]


def test_a_retriever_that_returns_nothing():
    cases = [{"question": "q", "relevant": ["p"]}]
    result = retrieval_hit_rate(cases, lambda q: [], 5)
    assert result["rate"] == 0.0 and result["misses"] == ["q"]


def test_misses_keep_the_case_order():
    cases = [{"question": "c", "relevant": ["q"]}, {"question": "a", "relevant": ["q"]}]
    assert retrieval_hit_rate(cases, retrieve, 3)["misses"] == ["c", "a"]
