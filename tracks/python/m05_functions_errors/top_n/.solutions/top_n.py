from collections.abc import Callable
from typing import Any


def top_n(items: list[Any], n: int, key: Callable[[Any], Any] | None = None) -> list[Any]:
    """Return the n largest items, largest first, compared by key if given."""
    if n <= 0:
        return []
    return sorted(items, key=key, reverse=True)[:n]
