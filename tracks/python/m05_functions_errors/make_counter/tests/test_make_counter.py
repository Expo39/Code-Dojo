from make_counter import make_counter


def test_counts_up():
    c = make_counter(5)
    assert [c(), c(), c()] == [5, 6, 7]


def test_default_start():
    assert make_counter()() == 0


def test_independent():
    a, b = make_counter(), make_counter(10)
    a(); a()
    assert b() == 10
    assert a() == 2
