from top_endpoints import top_endpoints


def test_example():
    lines = ["GET /a 200 5ms", "GET /b 200 3ms", "POST /a 201 9ms", "GET /b 500 1ms"]
    assert top_endpoints(lines, 2) == [("/a", 2), ("/b", 1)]


def test_ties_alphabetical():
    lines = ["GET /z 200 1ms", "GET /m 200 1ms", "GET /a 204 1ms"]
    assert top_endpoints(lines, 3) == [("/a", 1), ("/m", 1), ("/z", 1)]


def test_malformed_skipped():
    lines = ["garbage", "GET /a abc 1ms", "GET /a 200 1ms extra", "GET /ok 200 1ms"]
    assert top_endpoints(lines, 5) == [("/ok", 1)]


def test_n_larger_and_empty():
    assert top_endpoints([], 3) == []
