from compress import compress


def test_example():
    assert compress("aaabcc") == "a3b1c2"


def test_runs_repeat_later():
    assert compress("abca") == "a1b1c1a1"


def test_empty():
    assert compress("") == ""


def test_single_long_run():
    assert compress("zzzzzzzzzzzz") == "z12"
