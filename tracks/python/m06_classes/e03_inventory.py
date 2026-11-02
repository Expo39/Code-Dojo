"""Inventory.

Level: easy
Target: 20
Pattern: class-dict

class Inventory with:
- add(item, qty): qty > 0 else ValueError
- remove(item, qty): ValueError if qty <= 0 or more than in stock; an item that
  reaches 0 disappears from the inventory
- count(item): stock, 0 for unknown items
- total(): total number of units
- low_stock(threshold): sorted list of items with stock below threshold
"""


class Inventory:
    pass
