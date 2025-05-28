import jax.numpy as np
from jax import grad
from .estimators.__functions.__estimators import probability_y1
from .estimators.__prior import Prior
from jax.scipy.integrate import trapezoid
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
    """Calculate the information of a test item given the currently
    estimated ability `mu`.

    Args:
        mu (np.ndarray): currently estimated ability
        a (np.ndarray): _description_
        b (np.ndarray): _description_
        c (np.ndarray): _description_
        d (np.ndarray): _description_

    Returns:
        np.ndarray: _description_
    """
    p_y1 = probability_y1(mu, a, b, c, d)
    
    p_y1_grad = grad(lambda x: probability_y1(x, a, b, c, d))

    product = (p_y1_grad(mu) ** 2) / (p_y1 * (1 - p_y1))
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
    log_prior = lambda x: numpy.log(prior.pdf(x))
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
) -> np.ndarray:
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
        return item_information.sum() + prior_information
    else:
        return item_information.sum()
