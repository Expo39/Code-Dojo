import pytest
from split_bill import split_bill


def test_example_leftover_cent():
    assert split_bill(100, 15, 3) == [38.34, 38.33, 38.33]


def test_even_split():
    assert split_bill(50, 10, 4) == [13.75, 13.75, 13.75, 13.75]


def test_tip_with_fraction_of_a_cent():
    # 59.99 + 18% = 70.7882 -> 70.79, split in three
    shares = split_bill(59.99, 18, 3)
    assert shares == [23.60, 23.60, 23.59]
    assert round(sum(shares) * 100) == 7079


def test_amount_that_floats_cannot_store_exactly():
    assert split_bill(19.99, 0, 1) == [19.99]
    assert split_bill(0.29, 0, 2) == [0.15, 0.14]


def test_more_people_than_cents():
    assert split_bill(0.03, 0, 5) == [0.01, 0.01, 0.01, 0.0, 0.0]


def test_no_people():
    with pytest.raises(ValueError):
        split_bill(20, 10, 0)
