from ...models.__test_item import TestItem
from ...models.__item_selection_exception import ItemSelectionException
from ..estimators.__test_information import item_information_function
from ...models.__algorithm_exception import AlgorithmException
import numpy as np


def maximum_information_criterion(items: list[TestItem],
                                  ability: float) -> TestItem:
    """The maximum information criterion selected the next item for the respondent
    by finding the item that has the highest information value.

    Args:
        items (list[TestItem]): list of available items
        ability (float): currently estimated ability

    Returns:
        TestItem: item that has the highest information value

    Raises:
        ItemSelectionException: raised if no appropriate item was found
        AlgorithmException: raised if test information function could not be calculated
    """
    max_information = float("-inf")
    best_item = None

    for item in items:
        # extract parameters from the current item
        a = np.array([item.a])
        b = np.array([item.b])
        c = np.array([item.c])
        d = np.array([item.d])

        # calculate information for the current item
        try:
            information = float(item_information_function(
                mu=np.array(ability, dtype=float),
                a=a,
                b=b,
                c=c,
                d=d
            ))
            
            # if information is higher than before
            # set the item as new best item
            if information > max_information:
                max_information = information
                best_item = item
        except Exception as e:
            raise AlgorithmException(f"Error calculating test information: {e}")
        
    if best_item is None:
        raise ItemSelectionException("No appropriate item could be selected.")
    
    return best_item
