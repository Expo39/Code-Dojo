import pytest
from parse_pairs import parse_pairs


def test_example():
    assert parse_pairs("name Alice age 30\nname Bob city Rome") == [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "city": "Rome"},
    ]


def test_unknown_keys():
    assert parse_pairs("colour red size XL") == [{"colour": "red", "size": "XL"}]


def test_blank_lines_and_spaces():
    assert parse_pairs("\n  a 1   b 2  \n\n") == [{"a": "1", "b": "2"}]


def test_empty():
    assert parse_pairs("") == []


def test_odd_tokens():
    with pytest.raises(ValueError):
        parse_pairs("a 1 b")
