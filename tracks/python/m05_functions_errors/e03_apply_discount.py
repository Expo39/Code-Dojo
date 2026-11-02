"""Validated discount.

Level: tiny
Target: 5
Pattern: raise

Return price reduced by percent, rounded to 2 decimals. Raise ValueError if
price is negative or percent is outside 0 to 100.

    apply_discount(80, 25) -> 60.0
    apply_discount(19.99, 10) -> 17.99
"""


def apply_discount(price, percent):
    raise NotImplementedError
