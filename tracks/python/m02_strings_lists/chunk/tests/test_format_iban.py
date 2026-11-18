import pytest
from format_iban import format_iban


def test_example():
    assert format_iban("DE89370400440532", 4) == "DE89 3704 0044 0532"


def test_short_last_group():
    assert format_iban("NL91ABNA0", 4) == "NL91 ABNA 0"


def test_empty():
    assert format_iban("", 4) == ""


def test_size_bigger_than_code():
    assert format_iban("BE68", 10) == "BE68"


def test_bad_size():
    with pytest.raises(ValueError):
        format_iban("IT60X054", 0)


def test_size_three():
    assert format_iban("ES9121000", 3) == "ES9 121 000"
