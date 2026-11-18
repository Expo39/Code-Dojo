from count_calls import count_calls


def test_counts_and_returns():
    @count_calls
    def add(a, b=0):
        """Add."""
        return a + b

    assert add.calls == 0
    assert add(1, b=2) == 3
    assert add(5) == 5
    assert add.calls == 2


def test_keeps_metadata():
    @count_calls
    def greet():
        """Say hi."""

    assert greet.__name__ == "greet"
    assert greet.__doc__ == "Say hi."


def test_separate_counters():
    @count_calls
    def a():
        pass

    @count_calls
    def b():
        pass

    a()
    assert b.calls == 0
