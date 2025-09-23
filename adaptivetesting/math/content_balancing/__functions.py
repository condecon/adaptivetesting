from .__constraint import Constraint
from ...models.__test_item import TestItem
from ...models.__item_selection_exception import ItemSelectionException
from ...math.estimators.__test_information import item_information_function
import numpy as np


def compute_priority_index(item: TestItem,
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
        mu=np.array(current_ability, dtype=np.float64),
        a=np.array(item.a, dtype=np.float64),
        b=np.array(item.b, dtype=np.float64),
        c=np.array(item.c, dtype=np.float64),
        d=np.array(item.d, dtype=np.float64)
    ))

    return priority_index

    
def compute_quota_left(required_items: int,
                         shown_items: int) -> float:
    """
    Claculates the quota left (items left allowed to be shown) for a given constraint/group.

    Args:
        required_items (int): number of required items per constraint
        shown_items (int): number of already shown items per constraint

    Returns:
        float: calculated quota for the given constraint. Results in a float between 0 and 1.
        
    Example:
        `compute_quota_left(10, 8)`
    """
    quota = (required_items - shown_items) / required_items
    return quota


def compute_prop(n_administered: int,
                 prevalence: float,
                 n_remaining: int,
                 test_length: int) -> float:
    """Calculates the expected proportion
    of items with a specific constraint

    Args:
        n_administered (int): number of items constraint items administered
        prevalence (float): proportion of items in the pool with given constraint
        n_remaining (int): remaining items in pool with constraint 
        test_length (int): lenght of the test

    Returns:
        float: expected proportion
    """
    expected_proportion = (n_administered + prevalence * n_remaining) / test_length
    return expected_proportion

def compute_expected_difference(proportion: float,
                                constraint_target: float) -> float:
    """Calculates expected difference between
    expected proportion and the constraint target

    Args:
        proportion (float): expected proportion
        constraint_target (float): constraint target

    Returns:
        float: _description_
    """
    expected_difference = proportion - constraint_target
    return expected_difference

def compute_penalty_value(prop: float,
                          lower: float,
                          upper: float) -> float:
    """Calculates the penalty value for an item

    Args:
        prop (float): expected proportion
        lower (float): lower bound for proportion of items
        upper (float): upper bound for proportion of items

    Returns:
        float: penalty value
    """
    penalty_value: float = float("NaN")
    mid: float = (upper + lower) / 2

    if prop < lower:
        d = lower - mid
        k = 2
        penalty_value = ((1 / k * d) * 
                         (compute_expected_difference(proportion=prop, constraint_target=mid) ** 2) + 
                         (d / k))
        
    if prop >= upper:
        a = upper - mid
        k = 2
        penalty_value = ((1 / k * a) * 
                         (compute_expected_difference(proportion=prop, constraint_target=mid) ** 2) + 
                         (d / a))
        
    if upper > prop and prop >= lower:
        penalty_value = compute_expected_difference(proportion=prop,
                                                    constraint_target=mid)
        
    return penalty_value

def compute_total_content_penalty_value_for_item(item: TestItem,
                                         constraints: list[Constraint]) -> float:
    """Calculates the total content penalty value for a given item

    Args:
        item (TestItem): given test item
        group_weights (dict[str, float]): dictionary of group key and weight

    Returns:
        float: total content penalty value
    """
    assigned_item_constraints: list[str] = item.additional_properties["category"]
    assigned_constraints = [constraint for constraint in constraints if constraint.name in assigned_item_constraints]

    total_penalty_value = 0.0
    for constraint in assigned_constraints:
        total_penalty_value = total_penalty_value + compute_penalty_value(
            prop=constraint.proportion,
            lower=constraint.lower,
            upper=constraint.upper
        ) * constraint.weight
    
def standardize_total_content_constraint_penalty_value(item_penality_value: float,
                                               min: float,
                                               max: float) -> float:
    """Standardize total content contraint penalty values.

    Args:
        item_penality_value (float): unstandardized item penalty value
        min (float): minimum of the item penalty values over all eligible items
        max (float): maximum of the item penalty values over all eligible items

    Returns:
        float: standardized total content constraint penalty value
    """
    standardized_value = (item_penality_value - min) / (max - min)
    return standardized_value

def standardize_item_information(item_information: float,
                                 max: float) -> float:
    """Standardize the item information

    Args:
        item_information (float): information of an item
        max (float): maximum information value across all eligible items

    Returns:
        float: standardized item information
    """
    standardized_item_information = item_information / max
    return standardize_item_information

def compute_information_penalty_value(standardized_item_information: float) -> float:
    """Compute information penalty value with respect to the information

    Args:
        standardized_item_information (float): standardized item information

    Returns:
        float: information penalty
    """
    information_penalty = -(standardized_item_information ** 2)
    return information_penalty

def compute_weighted_penalty_value(constraint_weight: float,
                                   standardized_constraint_penalty_value: float,
                                   information_weight: float,
                                   information_penalty_value: float) -> float:
    """Calculates the weighted penalty value.
    The `constraint_weight` and `information_weight` parameters can be used
    to balance the content constraint and item information.

    Args:
        constraint_weight (float): constraint weight
        standardized_constraint_penalty_value (float): standardized constraint penalty value
        information_weight (float): information weight
        information_penalty_value (float): information penalty value

    Returns:
        float: weighted penalty value
    """
    weighted_penalty = constraint_weight * standardized_constraint_penalty_value + information_weight * information_penalty_value
    return weighted_penalty

