from ...models.__test_item import TestItem
from typing import List
from ...models.__item_selection_exception import ItemSelectionException


def urrys_rule(items: List[TestItem], ability: float) -> TestItem:
    """Urry's rule selects the test item
    which has the minimal difference between
    the item's difficulty and the ability level.

    Args:
        items (List[TestItem]): Test items (item pool)

        ability (float): Ability level (current ability estimation)

    Returns:
        TestItem: selected test item
    """
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

    raise ItemSelectionException("No appropriate item could be selected.")
