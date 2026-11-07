import pytest
from temperature import Temperature


def test_example():
    t = Temperature(25)
    assert t.kelvin == pytest.approx(298.15)
    t.kelvin = 373.15
    assert t.celsius == pytest.approx(100.0)


def test_default_and_celsius_assignment():
    t = Temperature()
    assert t.celsius == 0
    assert t.kelvin == pytest.approx(273.15)
    t.celsius = -40
    assert t.kelvin == pytest.approx(233.15)


def test_both_are_properties():
    assert isinstance(Temperature.celsius, property)
    assert isinstance(Temperature.kelvin, property)
    assert Temperature.kelvin.fset is not None


def test_below_absolute_zero_rejected_and_old_value_kept():
    t = Temperature(5)
    with pytest.raises(ValueError):
        t.celsius = -273.16
    assert t.celsius == 5
    with pytest.raises(ValueError):
        t.kelvin = -1
    assert t.celsius == 5


def test_constructor_validates_and_zero_point_allowed():
    with pytest.raises(ValueError):
        Temperature(-300)
    assert Temperature(-273.15).celsius == -273.15
    assert Temperature(-273.15).kelvin == pytest.approx(0.0)
