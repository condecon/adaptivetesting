from ...models.__test_item import TestItem

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
    ...


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
    ...