class Inventory:
    def __init__(self):
        self._stock = {}

    def add(self, item, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._stock[item] = self._stock.get(item, 0) + qty

    def remove(self, item, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        if qty > self.count(item):
            raise ValueError(f"only {self.count(item)} {item} in stock")
        self._stock[item] -= qty
        if self._stock[item] == 0:
            del self._stock[item]

    def count(self, item):
        return self._stock.get(item, 0)

    def total(self):
        return sum(self._stock.values())

    def low_stock(self, threshold):
        return sorted(item for item, qty in self._stock.items() if qty < threshold)
