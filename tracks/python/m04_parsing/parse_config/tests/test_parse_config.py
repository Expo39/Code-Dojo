import pytest
from parse_config import parse_config


def test_example():
    assert parse_config("# db\nhost = localhost\nport=5432\n") == {"host": "localhost", "port": 5432}


def test_last_wins_and_blank():
    assert parse_config("a = 1\n\n a = 2 ") == {"a": 2}


def test_equals_in_value():
    assert parse_config("query = a=b") == {"query": "a=b"}


def test_bad_line():
    with pytest.raises(ValueError):
        parse_config("no equals sign")
