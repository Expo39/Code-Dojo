from make_multipliers import make_multipliers


def test_each_function():
    fs = make_multipliers(4)
    assert [f(10) for f in fs] == [0, 10, 20, 30]
