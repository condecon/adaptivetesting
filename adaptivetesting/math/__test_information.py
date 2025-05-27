import jax.numpy as np
from jax import grad
from .estimators.__functions.__estimators import log_posterior as log_p
from .estimators.__functions.__estimators import posterior
from .estimators.__prior import Prior
from jax.scipy.integrate import trapezoid
from scipy.integrate import quad
import matplotlib.pyplot as plt


def test_information_function(
        mu: np.ndarray,
        a: np.ndarray,
        b: np.ndarray,
        c: np.ndarray,
        d: np.ndarray,
        response_pattern: np.ndarray,
        prior: Prior | None = None,
        optimization_interval: tuple[float, float] = (-10, 10)
) -> float:
    r"""
    Calculates test information.

    \[
    I{posterior}(\theta) = E{\theta|X}\left[ \left( \frac{\partial}{\partial \theta} \log p(\theta|X) \right)^2 \right]
    \]

    Args:
        mu (np.ndarray): ability level
        a (np.ndarray): discrimination parameter
        b (np.ndarray): difficulty parameter
        c (np.ndarray): guessing parameter
        d (np.ndarray): slipping parameter

    Returns:
        float: test information

    """
    log_posterior = lambda mu: log_p(mu, a, b, c, d, response_pattern, prior, border=optimization_interval)
    # calcualte first derivative of the log-likelihood function
    score_function = grad(log_posterior)

    # plot function
    x = np.linspace(optimization_interval[0], optimization_interval[1], 1000)  # shape (1000,)
    unnormal_posterior_values = np.array([posterior(xi, a, b, c, d, response_pattern, prior) for xi in x])
    evidence = trapezoid(unnormal_posterior_values, x)
    posterior_values = unnormal_posterior_values / evidence

    score_values = np.array([score_function(xi) for xi in x])
    information_values = (score_values ** 2) * posterior_values

    # calculate the mean of scoring_function ** 2
    information: np.ndarray = trapezoid(
        information_values,
        x
    )
    return information

