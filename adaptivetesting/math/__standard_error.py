import math
from typing import List
import jax.numpy as np
from .__test_information import test_information_function
from ..models.__test_item import TestItem


def standard_error(answered_items: List[TestItem], estimated_ability_level: float) -> float:
    """Calculates the standard error using the test information function.

    Args:
        answered_items (List[float]): List of answered items

        estimated_ability_level (float): Currently estimated ability level

    Returns:
        float: Standard error
    """
    a=np.array([item.a for item in answered_items])   
    b=np.array([item.b for item in answered_items])
    c=np.array([item.c for item in answered_items])
    d=np.array([item.d for item in answered_items])

    error = 1 / math.sqrt(test_information_function(mu=np.array(estimated_ability_level),
                                                    a=a,
                                                    b=b,
                                                    c=c,
                                                    d=d
                                                    ))

    return error
