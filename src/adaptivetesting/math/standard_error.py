import math
from typing import List
import numpy as np
from .test_information import test_information_function


def standard_error(answered_items: List[float],
                   estimated_ability_level: float) -> float:
    """Calculates standard error using test information function.

    Args:
        answered_items (List[TestItem]): List of answered items
        estimated_ability_level (float): Currently estimated ability level

    Returns:
        float: Standard error
    """

    answered_items_array = np.array(answered_items, dtype="float64")
    estimated_ability_level_array = np.array(estimated_ability_level, dtype="float64")  # noqa E501
    test_information = test_information_function(answered_items_array, estimated_ability_level_array)  # noqa E501

    error = 1 / math.sqrt(test_information)

    return error
