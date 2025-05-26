import jax.numpy as np
from jax import grad
from .estimators.__functions.__estimators import posterior as p
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
    """
    Calculates test information.

    Args:
        mu (np.ndarray): ability level
        a (np.ndarray): discrimination parameter
        b (np.ndarray): difficulty parameter
        c (np.ndarray): guessing parameter
        d (np.ndarray): slipping parameter

    Returns:
        float: test information

    """
    posterior = lambda mu: p(mu, a, b, c, d, response_pattern, prior, border=optimization_interval)
    # calcualte first derivative of the log-likelihood function
    score_function = grad(posterior)

    # plot function
    x = np.linspace(-10, 10, 1000)  # shape (1000,)
    post_values = np.array([posterior(xi) for xi in x])
    score_values = np.array([score_function(xi) for xi in x])
    plt.plot(x, post_values, label="Posterior")
    plt.plot(x, score_values, label="Score function")
    plt.legend()
    plt.show()
    
    print(f"Mean: {np.mean(score_values**2)}")
    print(f"Mean: {np.var(score_values)}")

    # calculate the mean of the (score function)**2
    # This is the expected Fisher information over the interval
    numerator, _ = quad(
        lambda x: score_function(x) ** 2 * posterior(x),
        a=optimization_interval[0],
        b=optimization_interval[1],
        limit=400
    )

    denominator, _ = quad(
        lambda x: posterior(x),
        a=optimization_interval[0],
        b=optimization_interval[1],
        limit=400
    )
    
    return numerator / denominator

