from find_dates import find_dates


def test_example():
    assert find_dates("Shipped 2024-03-15, delivered 2024-03-18.") == [
        (2024, 3, 15),
        (2024, 3, 18),
    ]


def test_returns_ints():
    [(year, month, day)] = find_dates("on 2021-07-04")
    assert (year, month, day) == (2021, 7, 4)
    assert all(isinstance(x, int) for x in (year, month, day))


def test_impossible_month_or_day():
    text = "bad 2024-13-01 bad 2024-00-10 bad 2024-05-32 bad 2024-05-00 ok 2024-12-31"
    assert find_dates(text) == [(2024, 12, 31)]


def test_inside_longer_numbers():
    assert find_dates("ref 12024-01-05 and 2024-01-055 and 2024-1-5") == []


def test_punctuation_around_counts():
    assert find_dates("backup (2025-02-28), next on 2025-03-07.") == [(2025, 2, 28), (2025, 3, 7)]


def test_no_dates():
    assert find_dates("") == []
    assert find_dates("call 555-1234 at 10") == []
