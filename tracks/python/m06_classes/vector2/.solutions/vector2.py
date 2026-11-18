import math
from dataclasses import dataclass


@dataclass
class Vector2:
    x: float
    y: float

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, factor):
        return Vector2(self.x * factor, self.y * factor)

    def length(self):
        return math.hypot(self.x, self.y)
