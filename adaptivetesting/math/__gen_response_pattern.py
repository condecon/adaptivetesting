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
        rng = np.random.RandomState(seed)
    else:
        rng = np.random.RandomState()

    responses: list[int] = []

    for item in items:
        probability_of_success = probability_y1(mu=np.array(ability),
                                                a=np.array(item.a),
                                                b=np.array(item.b),
                                                c=np.array(item.c),
                                                d=np.array(item.d))
        
        # Handle numpy scalar/array return properly
        if hasattr(probability_of_success, 'item'):
            prob_scalar = probability_of_success.item()
        else:
            prob_scalar = float(probability_of_success)
        
        # Validate probability bounds
        if not (0 <= prob_scalar <= 1):
            raise ValueError(f"Invalid probability: {prob_scalar}. Must be between 0 and 1.")
        
        # simulate response based on probability of success
        random_val = rng.random_sample()
        response = 1 if random_val < prob_scalar else 0
        responses.append(response)

    return responses
