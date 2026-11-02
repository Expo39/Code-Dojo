import pytest
from apply_discount import apply_discount


def test_examples():
    assert apply_discount(80, 25) == 60.0
    assert apply_discount(19.99, 10) == 17.99


def test_bounds_ok():
    assert apply_discount(10, 0) == 10
    assert apply_discount(10, 100) == 0


@pytest.mark.parametrize("price,percent", [(-1, 10), (10, -5), (10, 101)])
def test_invalid(price, percent):
    with pytest.raises(ValueError):
        apply_discount(price, percent)
