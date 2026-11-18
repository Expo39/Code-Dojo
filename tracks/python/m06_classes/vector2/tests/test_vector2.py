from vector2 import Vector2


def test_add_and_eq():
    assert Vector2(1, 2) + Vector2(3, 4) == Vector2(4, 6)


def test_scale():
    assert Vector2(1, -2) * 3 == Vector2(3, -6)


def test_length():
    assert Vector2(3, 4).length() == 5.0


def test_repr():
    assert repr(Vector2(1, 2)) == "Vector2(x=1, y=2)"


def test_immutable_inputs():
    a = Vector2(1, 1)
    b = a + a
    assert a == Vector2(1, 1) and b == Vector2(2, 2)
