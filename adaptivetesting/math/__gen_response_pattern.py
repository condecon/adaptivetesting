from .estimators.__functions.__estimators import probability_y1
from ..models.__test_item import TestItem
import numpy as np


def generate_response_pattern(ability: float,
                              items: list[TestItem],
                              seed: int | None = None) -> list[int]:
    """Generates a response pattern for a given ability level
    and item difficulties. Also, a seed can be set.

    Args:
        ability (float): participants ability
        items (list[TestItem]): test items
        seed (int, optional): Seed for the random process.

    Returns:
        list[int]: response pattern
    """
    # Set seed once at the beginning if provided
    if seed is not None:
        np.random.seed(seed)
    
    responses: list[int] = []

    for item in items:
        probability_of_success = probability_y1(mu=np.array(ability),
                                                a=np.array(item.a),
                                                b=np.array(item.b),
                                                c=np.array(item.c),
                                                d=np.array(item.d))
        
        # Ensure probability is a scalar value
        prob_scalar = float(probability_of_success)
        
        # simulate response based on probability of success
        response = int(np.random.binomial(n=1, p=prob_scalar))
        responses.append(response)

    return responses
