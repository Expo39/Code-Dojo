import pytest
from days_between import days_between, weekday_name


def test_days():
    assert days_between("02/11/2026", "25/12/2026") == 53
    assert days_between("25/12/2026", "02/11/2026") == -53
    assert days_between("28/02/2028", "01/03/2028") == 2


def test_weekday():
    assert weekday_name("02/11/2026") == "Monday"
    assert weekday_name("08/11/2026") == "Sunday"


def test_day_first_not_month_first():
    assert days_between("01/02/2026", "01/03/2026") == 28


def test_invalid():
    with pytest.raises(ValueError):
        days_between("30/02/2026", "01/03/2026")
