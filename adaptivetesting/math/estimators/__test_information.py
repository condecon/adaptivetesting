import jax.numpy as jnp
from jax import grad
from .__functions.__estimators import probability_y1
from .__prior import Prior
from jax.scipy.integrate import trapezoid
import numpy
from scipy.differentiate import derivative


def item_information_function(
        mu: jnp.ndarray,
        a: jnp.ndarray,
        b: jnp.ndarray,
        c: jnp.ndarray,
        d: jnp.ndarray
) -> jnp.ndarray:
    """Calculate the information of a test item given the currently
    estimated ability `mu`.

    Args:
        mu (jnp.ndarray): currently estimated ability
        a (jnp.ndarray): _description_
        b (jnp.ndarray): _description_
        c (jnp.ndarray): _description_
        d (jnp.ndarray): _description_

    Returns:
        jnp.ndarray: _description_
    """
    p_y1 = probability_y1(mu, a, b, c, d)
    
    p_y1_grad = grad(lambda x: probability_y1(x, a, b, c, d))

    product = (p_y1_grad(mu) ** 2) / (p_y1 * (1 - p_y1))
    information = jnp.sum(product)
    return information


def prior_information_function(prior: Prior,
                               optimization_interval: tuple[float, float] = (-10, 10)) -> jnp.ndarray:
    """Calculates the fisher information for the probability density function
    of the specified prior

    Args:
        prior (Prior): _description_

    Returns:
        jnp.ndarray: _description_
    """
    def log_prior(x):
        epsilon = 1e-12  # Small value to avoid log(0)
        return numpy.log(prior.pdf(x) + epsilon)
    x_vals = jnp.linspace(optimization_interval[0], optimization_interval[1], 1000)
    score_values = jnp.array(derivative(log_prior, x_vals).df)

    information = trapezoid(
        (score_values ** 2) * prior.pdf(x_vals),
        x_vals
    )
    
    return information


def test_information_function(
        mu: jnp.ndarray,
        a: jnp.ndarray,
        b: jnp.ndarray,
        c: jnp.ndarray,
        d: jnp.ndarray,
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
        mu (jnp.ndarray): ability level
        a (jnp.ndarray): discrimination parameter
        b (jnp.ndarray): difficulty parameter
        c (jnp.ndarray): guessing parameter
        d (jnp.ndarray): slipping parameter

    Returns:
        float: test information
    """
    # calcualte information for every item
    item_information = jnp.vectorize(item_information_function)(
        mu, a, b, c, d
    )

    if prior:
        prior_information = prior_information_function(prior, optimization_interval)
        return float(item_information.sum() + prior_information)
    else:
        return float(item_information.sum())
