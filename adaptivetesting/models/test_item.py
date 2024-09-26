from typing import Any, Dict, List
from dataclasses import dataclass


class TestItem:
    """Representation of a test item in the item pool.
    The format is equal to the implementation in catR.
    """
    def __init__(self):
        self.id: int = None
        self.a: float = 1
        self.b: float = None
        self.c: float = 0
        self.d: float = 1


def load_test_items_from_list(source: List[float]) -> List[TestItem]:
    """Creates test items from a list of floats.

    Args:
        source (List[float]): Item difficulties

    Returns:
        List[TestItem]: item pool
    """
    items: List[TestItem] = []

    for difficulty in source:
        item = TestItem()
        item.b = difficulty
        items.append(item)

    return items
