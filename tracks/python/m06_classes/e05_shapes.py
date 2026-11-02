"""Inheritance.

Level: easy
Target: 15
Pattern: inheritance

Write class Rectangle(width, height) with area(), perimeter() and repr
"Rectangle(2, 3)". Write class Square(side) that INHERITS from Rectangle and
reuses its methods (call super().__init__); its repr is "Square(4)".
"""


class Rectangle:
    pass


class Square(Rectangle):
    pass
