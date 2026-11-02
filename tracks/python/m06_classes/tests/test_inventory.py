import pytest
from inventory import Inventory


def test_add_count_total():
    inv = Inventory()
    inv.add("bolt", 10)
    inv.add("nut", 3)
    inv.add("bolt", 5)
    assert inv.count("bolt") == 15
    assert inv.count("washer") == 0
    assert inv.total() == 18


def test_remove():
    inv = Inventory()
    inv.add("nut", 3)
    inv.remove("nut", 3)
    assert inv.count("nut") == 0
    assert inv.low_stock(1) == []


def test_remove_too_many():
    inv = Inventory()
    inv.add("nut", 3)
    with pytest.raises(ValueError):
        inv.remove("nut", 4)
    with pytest.raises(ValueError):
        inv.remove("ghost", 1)
    assert inv.count("nut") == 3


def test_low_stock_sorted():
    inv = Inventory()
    for item, qty in [("z", 1), ("a", 2), ("m", 9)]:
        inv.add(item, qty)
    assert inv.low_stock(5) == ["a", "z"]


def test_bad_qty():
    with pytest.raises(ValueError):
        Inventory().add("x", 0)
