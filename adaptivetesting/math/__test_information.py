## CHANGE
# Hier geht irgendwas schief, glaube ich....

import jax.numpy as np


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
    p_right = c + (d - c) * \
        (np.exp(a * (mu - b))) / \
        (1 + np.exp(a * (mu - b)))
    
    p_wrong = c + (d - c) * \
        1 / (1 + np.exp(a * (mu - b)))

    product = p_right * p_wrong
    information_tensor = np.cumsum(product)
    information = information_tensor[len(information_tensor) - 1]
    # convert information to float and return
    return float(information)

