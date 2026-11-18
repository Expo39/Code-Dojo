import pytest
from ticket_machine import Queue, Ticket


@pytest.fixture(autouse=True)
def fresh_numbers():
    Ticket.reset_numbers()


def test_example():
    q = Queue()
    q.take("Ann")
    q.take("Bo")
    assert q.serve_next().number == 1
    assert q.waiting() == ["Bo"]
    assert len(q) == 1


def test_numbers_shared_across_queues_and_tickets():
    a, b = Queue(), Queue()
    first = a.take("Cy")
    second = b.take("Di")
    loose = Ticket("Gus")
    third = a.take("Ed")
    assert (first.number, second.number, loose.number, third.number) == (1, 2, 3, 4)
    assert first.name == "Cy"
    assert len(a) == 2 and len(b) == 1


def test_counter_lives_on_the_class_and_resets():
    Ticket("x")
    Ticket("y")
    Ticket.reset_numbers()
    assert Ticket("z").number == 1
    assert "reset_numbers" in vars(Ticket)
    assert isinstance(vars(Ticket)["reset_numbers"], classmethod)


def test_composition_not_inheritance():
    assert not issubclass(Queue, list)
    q = Queue()
    assert len(q) == 0
    assert q.waiting() == []


def test_waiting_returns_a_copy_and_queues_are_separate():
    a, b = Queue(), Queue()
    a.take("Ann")
    names = a.waiting()
    names.append("intruder")
    assert a.waiting() == ["Ann"]
    assert b.waiting() == []


def test_serve_empty_raises_and_fifo_order():
    q = Queue()
    with pytest.raises(IndexError):
        q.serve_next()
    for name in ["A", "B", "C"]:
        q.take(name)
    assert [q.serve_next().name for _ in range(3)] == ["A", "B", "C"]
    assert len(q) == 0
