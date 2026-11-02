import pytest
from stack import Stack


def test_push_pop_order():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2
    assert s.pop() == 1


def test_peek_and_len():
    s = Stack()
    s.push("a")
    assert s.peek() == "a"
    assert len(s) == 1
    assert not s.is_empty()


def test_empty_errors():
    s = Stack()
    assert s.is_empty()
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.peek()


def test_instances_separate():
    a, b = Stack(), Stack()
    a.push(1)
    assert len(b) == 0
