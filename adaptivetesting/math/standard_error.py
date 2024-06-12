import math
from typing import List
import numpy as np
from .test_information import test_information_function


def standard_error(answered_items: List[float], estimated_ability_level: float) -> float:
    """Calculates standard error using test information function.

    Args:
        answered_items (List[float]): List of answered items

        estimated_ability_level (float): Currently estimated ability level

    Returns:
        float: Standard error
    """
    error = 1 / math.sqrt(test_information_function(np.array(answered_items, dtype="float64"),
                                                               np.array(estimated_ability_level, dtype="float64")))

    return error
