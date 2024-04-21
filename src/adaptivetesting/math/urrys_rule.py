from ..models.test_item import TestItem
from typing import List


def urrys_rule(items: List[TestItem], ability: float) -> TestItem:
    # create difference array from absolute value
    difference: List[float] = []

    for item in items:
        difference.append(abs(ability - item.b))

    # get minimal difference
    minimal_difference = min(difference)

    # find the item where minimal difference is equal to absolut
    # value of difference
    for item in items:
        if abs(ability - item.b) == minimal_difference:
            return item
