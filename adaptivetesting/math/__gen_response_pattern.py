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
    responses: list[int] = []

    for item in items:
        probability_of_success = probability_y1(mu=ability,
                                                a=item.a,
                                                b=item.b,
                                                c=item.c,
                                                d=item.d)
        
        # simulate response based on probability of scucess
        if seed is not None:
            np.random.seed(seed)
        response = np.random.binomial(n=1, p=probability_of_success)
        responses.append(response)

    return responses
