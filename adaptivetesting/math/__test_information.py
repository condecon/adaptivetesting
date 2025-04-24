import jax.numpy as np
from .estimators.__functions.__estimators import probability_y1
from scipy.differentiate import derivative


def test_information_function(
        mu: np.ndarray,
        a: np.ndarray,
        b: np.ndarray,
        c: np.ndarray,
        d: np.ndarray,
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
    p_y1 = probability_y1(mu, a, b, c, d)
    
    p_y1_grad = derivative(probability_y1,
                           mu,
                           args=(a, b, c, d))

    product = (p_y1_grad.df ** 2) / (p_y1 * (1 - p_y1))
    information_tensor = np.cumsum(product)
    information = information_tensor[len(information_tensor) - 1]
    # convert information to float and return
    return float(information)
