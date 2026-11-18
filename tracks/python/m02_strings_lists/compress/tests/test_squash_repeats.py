from squash_repeats import squash_repeats


def test_example():
    assert squash_repeats(["boot", "ping", "ping", "ping", "halt"]) == [
        "boot", "ping (x3)", "halt"
    ]


def test_message_returns_later():
    assert squash_repeats(["a", "a", "b", "a"]) == ["a (x2)", "b", "a"]


def test_run_at_the_end():
    assert squash_repeats(["start", "tick", "tick"]) == ["start", "tick (x2)"]


def test_empty():
    assert squash_repeats([]) == []


def test_input_unchanged():
    lines = ["x", "x"]
    squash_repeats(lines)
    assert lines == ["x", "x"]
