from shapes import Rectangle, Square


def test_rectangle():
    r = Rectangle(2, 3)
    assert r.area() == 6
    assert r.perimeter() == 10
    assert repr(r) == "Rectangle(2, 3)"


def test_square_reuses():
    s = Square(4)
    assert s.area() == 16
    assert s.perimeter() == 16
    assert isinstance(s, Rectangle)
    assert repr(s) == "Square(4)"


def test_no_duplicate_methods():
    assert "area" not in Square.__dict__
    assert "perimeter" not in Square.__dict__
