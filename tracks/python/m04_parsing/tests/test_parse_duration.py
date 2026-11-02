import pytest
from parse_duration import parse_duration


def test_examples():
    assert parse_duration("1h30m") == 5400
    assert parse_duration("45m") == 2700
    assert parse_duration("2h") == 7200
    assert parse_duration("90s") == 90
    assert parse_duration("1h2m3s") == 3723


@pytest.mark.parametrize("bad", ["", "10", "5x", "m5", "1m1h", "1h1h"])
def test_invalid(bad):
    with pytest.raises(ValueError):
        parse_duration(bad)
