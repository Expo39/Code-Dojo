import pytest
from temperature import Temperature


def test_example():
    t = Temperature(25)
    assert t.fahrenheit == pytest.approx(77.0)
    t.fahrenheit = 212
    assert t.celsius == pytest.approx(100.0)


def test_default_and_celsius_assignment():
    t = Temperature()
    assert t.celsius == 0
    assert t.fahrenheit == pytest.approx(32.0)
    t.celsius = -40
    assert t.fahrenheit == pytest.approx(-40.0)


def test_both_are_properties():
    assert isinstance(Temperature.celsius, property)
    assert isinstance(Temperature.fahrenheit, property)
    assert Temperature.fahrenheit.fset is not None


def test_below_absolute_zero_rejected_and_old_value_kept():
    t = Temperature(5)
    with pytest.raises(ValueError):
        t.celsius = -273.16
    assert t.celsius == 5
    with pytest.raises(ValueError):
        t.fahrenheit = -500
    assert t.celsius == 5


def test_constructor_validates_and_zero_point_allowed():
    with pytest.raises(ValueError):
        Temperature(-300)
    assert Temperature(-273.15).celsius == -273.15
