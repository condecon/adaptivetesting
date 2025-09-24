import numpy as np
from .__functions.__estimators import probability_y1
from .__prior import Prior
from scipy.integrate import trapezoid
import numpy
from scipy.differentiate import derivative


def item_information_function(
        mu: np.ndarray,
        a: np.ndarray,
        b: np.ndarray,
        c: np.ndarray,
        d: np.ndarray
) -> np.ndarray:
    p_y1 = probability_y1(mu, a, b, c, d)

    # Clip probabilities
    p_y1_clipped = np.clip(p_y1, 1e-10, 1 - 1e-10)

    def p_y1_grad(x: np.ndarray) -> np.ndarray:
        # Use a more robust finite difference scheme
        h = np.maximum(1e-8, 1e-8 * np.abs(x))  # Adaptive step size
        return (probability_y1(x + h, a, b, c, d) - probability_y1(x - h, a, b, c, d)) / (2 * h)

    product = (p_y1_grad(mu) ** 2) / (p_y1_clipped * (1 - p_y1_clipped))
    information = np.sum(product)
    return information


def prior_information_function(prior: Prior,
                               optimization_interval: tuple[float, float] = (-10, 10)) -> np.ndarray:
    """Calculates the fisher information for the probability density function
    of the specified prior

    Args:
        prior (Prior): _description_

    Returns:
        np.ndarray: _description_
    """
    def log_prior(x):
        epsilon = 1e-12  # Small value to avoid log(0)
        return numpy.log(prior.pdf(x) + epsilon)
    x_vals = np.linspace(optimization_interval[0], optimization_interval[1], 1000)
    score_values = np.array(derivative(log_prior, x_vals).df)

    information = trapezoid(
        (score_values ** 2) * prior.pdf(x_vals),
        x_vals
    )

    return information


def test_information_function(
        mu: np.ndarray,
        a: np.ndarray,
        b: np.ndarray,
        c: np.ndarray,
        d: np.ndarray,
        prior: Prior | None = None,
        optimization_interval: tuple[float, float] = (-10, 10)
) -> float:
    """
    Calculates test information.
    Therefore, the information is calculated for every item
    and then summed up.
    If a prior is specified, the fisher information of the prior
    is calculated as well and added to the information sum.

    Args:
        mu (np.ndarray): ability level
        a (np.ndarray): discrimination parameter
        b (np.ndarray): difficulty parameter
        c (np.ndarray): guessing parameter
        d (np.ndarray): slipping parameter

    Returns:
        float: test information
    """
    # calcualte information for every item
    item_information = np.vectorize(item_information_function)(
        mu, a, b, c, d
    )

    if prior:
        prior_information = prior_information_function(prior, optimization_interval)
        return float(item_information.sum() + prior_information)
    else:
        return float(item_information.sum())
