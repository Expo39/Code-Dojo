from same_serial import same_serial


def test_example():
    assert same_serial("AB-12 cd", "ab12CD") is True


def test_different_order():
    assert same_serial("AB-12", "AB-21") is False


def test_digits_matter():
    assert same_serial("A1", "A7") is False
    assert same_serial("A-1", "a 1") is True


def test_extra_character():
    assert same_serial("AB12", "AB12C") is False


def test_empty_and_symbols():
    assert same_serial("", "") is True
    assert same_serial("--", " ") is True
