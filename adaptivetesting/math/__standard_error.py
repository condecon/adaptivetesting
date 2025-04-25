import math
from typing import List, Literal
import jax.numpy as np
from .__test_information import test_information_function
from ..models.__test_item import TestItem


def standard_error(answered_items: List[TestItem],
                   estimated_ability_level: float,
                   estimator: Literal["ML", "BM"] = "ML",
                   sd: float | None = None) -> float:
    """Calculates the standard error using the test information function.
    If Bayes Modal is used for the ability estimation, a standard deviation value
    of the prior distribution has to be provided.

    Args:
        answered_items (List[float]): List of answered items

        estimated_ability_level (float): Currently estimated ability level

        estimator (Literal["ML", "BM"]): Ability estimator (Default: ML)

        sd (float | None): Standard deviation of the prior distribution. Only required for BM.

    Raises:
        ValueError
    
    Returns:
        float: Standard error
    """
    a = np.array([item.a for item in answered_items])
    b = np.array([item.b for item in answered_items])
    c = np.array([item.c for item in answered_items])
    d = np.array([item.d for item in answered_items])

    if estimator == "ML":
        error = 1 / math.sqrt(test_information_function(mu=np.array(estimated_ability_level),
                                                        a=a,
                                                        b=b,
                                                        c=c,
                                                        d=d
                                                        ))

        return error
    
    if estimator == "BM":
        information = test_information_function(mu=np.array(estimated_ability_level),
                                                a=a,
                                                b=b,
                                                c=c,
                                                d=d)

        if sd is None:
            raise ValueError("sd cannot be None if BM is used as estimator.")
        
        error = 1 / math.sqrt(
            (1 / math.pow(sd, 2)) + information
        )

        return error
