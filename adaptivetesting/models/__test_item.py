from typing import Any, Dict, List
from dataclasses import dataclass


class TestItem:
    def __init__(self):
        """Representation of a test item in the item pool.
        The format is equal to the implementation in catR.

        ## Properties:
            - a (float):
            - b (float): difficulty
            - c (float): 
            - d (float):

        """
        self.id: int | None = None
        self.a: float = 1
        self.b: float = float("nan")
        self.c: float = 0
        self.d: float = 1
    
    def as_dict(self) -> dict[str, float]:
        return {
            "a": self.a,
            "b": self.b,
            "c": self.c,
            "d": self.d
        }


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

def load_test_items_from_dict(source: dict[str, List[float]]) -> List[TestItem]:
    """Creates test items from a dictionary.
    The dictionary has to have the following keys:
        
        - a
        - b
        - c
        - d
    each containing a list of float.

    Args:
        source (dict[str, List[float]]): item pool dictionary

    Returns:
        List[TestItem]: item pool
    """
    a = source.get("a")
    b = source.get("b")
    c = source.get("c")
    d = source.get("d")

    # check none
    if a is None:
        raise ValueError("a cannot be None")
    
    if b is None:
        raise ValueError("b cannot be None")
    
    if c is None:
        raise ValueError("c cannot be None")
    
    if d is None:
        raise ValueError("d cannot be None")

    # check if a, b, c, and d have the same length
    if not (len(a) == len(b) == len(c) == len(d)):
        raise ValueError("All lists in the source dictionary must have the same length")

    n_items = len(b)
    items: List[TestItem] = []
    for i in range(n_items):
        item = TestItem()
        item.a = a[i]
        item.b = b[i]
        item.c = c[i]
        item.d = d[i]

        items.append(item)

    return items

