from .estimators.__functions.__estimators import probability_y1
from .estimators.__functions.__poly.__gpcm import GPCM
from .estimators.__functions.__poly.__grm import GRM
from ..models.__test_item import TestItem
import numpy as np
from typing import Literal, cast
from scipy.stats import multinomial
from scipy.special import softmax


def generate_response_pattern(ability: float,
                              items: list[TestItem],
                              model: Literal["GRM", "GPCM"] | None = None,
                              seed: int | None = None) -> list[int]:
    """Generates a response pattern for a given ability level
    and item difficulties. Also, a seed can be set.

    Args:
        ability (float): participants ability
        items (list[TestItem]): test items
        model (Literal["GRM", "GPCM"], optional): model type (required for polytomous models)
        seed (int, optional): Seed for the random process.

    Returns:
        list[int]: response pattern
    """
    # Set seed once at the beginning if provided
    if seed is not None:
        rng = np.random.RandomState(seed)
    else:
        rng = np.random.RandomState()

    if all([item.is_polytomous() for item in items]):
        if model is None:
            raise ValueError("model has to be specified for polytomous items")
        else:
            return gen_pattern_poly(
                ability,
                items,
                model,
                rng
            )
    else:
        return gen_pattern_dichotomous(ability,
                                       items,
                                       rng)


def gen_pattern_dichotomous(ability: float,
                            items: list[TestItem],
                            rng: np.random.RandomState):
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


def gen_pattern_poly(
    ability: float,
    items: list[TestItem],
    model: Literal["GRM", "GPCM"],
    rng: np.random.RandomState
) -> list[int]:
    responses: list[int] = []
    # loop through all items
    for item in items:
        # calculate probability for every class
        log_probabilities: list[float] = []
        if model == "GRM":
            for t_i in range(len(cast(list, item.b)) + 1):
                log_prob = GRM.category_prob(ability,
                                         item.a,
                                         cast(list, item.b),
                                         response_pattern=t_i)
                log_probabilities.append(log_prob)
        elif model == "GPCM":
            for t_i in range(len(cast(list, item.b)) + 1):
                log_prob = GPCM.category_prob(ability,
                                          item.a,
                                          cast(list, item.b),
                                          response_pattern=t_i)
                log_probabilities.append(log_prob)

        

        # draw from multinomial distribution for final response
        # the probability for a response in k categories is 1
        probabilities = softmax(np.array(log_probabilities))
        mn_draw = cast(np.ndarray, multinomial.rvs(
            n=1,
            p=probabilities,
            size=(),
            random_state=rng
        )).astype(int)
        response = np.argmax(mn_draw).item()
        responses.append(response)

    return responses
