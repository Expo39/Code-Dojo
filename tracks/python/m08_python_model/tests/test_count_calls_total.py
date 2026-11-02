import count_calls_total as m


def test_counts():
    m.total_calls = 0
    assert m.record_call() == 1
    assert m.record_call() == 2
    assert m.total_calls == 2
