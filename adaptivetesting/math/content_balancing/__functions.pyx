from ...models.__test_item import TestItem
from ...models.__item_selection_exception import ItemSelectionException
from ...math.estimators.__test_information import item_information_function
import numpy as np

def calculate_priority_index(item: TestItem,
                             group_weights: dict[str, float],
                             required_items: int,
                             shown_item: int,
                             current_ability: float) -> float:
    """Calculates the priority index of a given item.

    Args:
        item (TestItem): Item for which to calcualte the priority index
        group_weights (dict[str, float]): Dictionary with the group names and their weights
            Example: `{"math": 1, "english": 1}`. These weight show how important a specific
            constraint is for the item selection process
        required_items (int): number of items required to be shown per constraint
        shown_item (int): number of items already shown per constraint

    Returns:
        float: priority index of an item

    Raises:
        ItemSelectionException: Raised if the additional properties of the items are not correctly formatted.
    """
    try:
        item_groups: list[str] = item.additional_properties["category"]

        if not isinstance(item_groups, list):
            raise ItemSelectionException("Additional properties of the items are not correctly formatted.")
    except KeyError:
        raise ItemSelectionException("Additional properties of the items are not correctly formatted.")
    priority_index: float = 1.0

    for group in item_groups:
        priority_index = priority_index * group_weights[group] * calculate_quota_left(required_items=required_items, shown_items=shown_item)
    
    # weight fisher information
    priority_index = priority_index * float(item_information_function(
        mu=np.array(current_ability),
        a=np.array(item.a),
        b=np.array(item.b),
        c=np.array(item.c),
        d=np.array(item.d)
    ))

    return priority_index

    
def calculate_quota_left(required_items: int,
                         shown_items: int) -> float:
    """
    Claculates the quota left (items left allowed to be shown) for a given constraint/group.

    Args:
        required_items (int): number of required items per constraint
        shown_items (int): number of already shown items per constraint

    Returns:
        float: calculated quota for the given constraint. Results in a float between 0 and 1.
        
    Example:
        `calculate_quota_left(10, 8)`
    """
    quota = (required_items - shown_items) / required_items
    return quota
