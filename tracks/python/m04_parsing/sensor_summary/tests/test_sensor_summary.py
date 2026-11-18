from sensor_summary import sensor_summary


def test_example():
    text = "t1,2026-11-02T10:00,20\nt1,2026-11-02T10:05,22\nt2,2026-11-02T10:00,5"
    assert sensor_summary(text) == {
        "t1": {"count": 2, "min": 20.0, "max": 22.0, "avg": 21.0},
        "t2": {"count": 1, "min": 5.0, "max": 5.0, "avg": 5.0},
    }


def test_bad_values_skipped():
    text = "a,x,1\na,x,oops\n\na,x,2"
    assert sensor_summary(text) == {"a": {"count": 2, "min": 1.0, "max": 2.0, "avg": 1.5}}


def test_rounding():
    assert sensor_summary("s,t,1\ns,t,1\ns,t,2")["s"]["avg"] == 1.33


def test_empty():
    assert sensor_summary("") == {}
