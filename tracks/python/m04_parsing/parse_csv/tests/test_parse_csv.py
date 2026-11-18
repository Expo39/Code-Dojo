import pytest
from parse_csv import parse_csv


def test_example():
    assert parse_csv("name, qty\napple, 3\npear,5") == [
        {"name": "apple", "qty": "3"},
        {"name": "pear", "qty": "5"},
    ]


def test_blank_lines():
    assert parse_csv("\na,b\n\n1,2\n") == [{"a": "1", "b": "2"}]


def test_header_only_and_empty():
    assert parse_csv("a,b") == []
    assert parse_csv("") == []


def test_bad_row_line_number():
    with pytest.raises(ValueError, match="3"):
        parse_csv("a,b\n1,2\n1,2,3")
