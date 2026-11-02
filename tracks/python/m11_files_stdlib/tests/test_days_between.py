import pytest
from days_between import days_between, weekday_name


def test_days():
    assert days_between("2026-11-02", "2026-12-25") == 53
    assert days_between("2026-12-25", "2026-11-02") == -53
    assert days_between("2028-02-28", "2028-03-01") == 2


def test_weekday():
    assert weekday_name("2026-11-02") == "Monday"
    assert weekday_name("2026-11-08") == "Sunday"


def test_invalid():
    with pytest.raises(ValueError):
        days_between("2026-02-30", "2026-03-01")
