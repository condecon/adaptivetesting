import numpy as np


def test_information_function(
        item_difficulties: np.ndarray,
        ability_level: np.ndarray
) -> float:
    """
    Calculates test information.

    Args:
        item_difficulties (np.ndarray): List of answered items

        ability_level (np.ndarray): Currently estimated ability level

    Returns:
        float: test information

    """
    p_right = (np.exp(item_difficulties - ability_level)) / (
            1 + np.exp(item_difficulties - ability_level))
    p_wrong = 1 / (1 + np.exp(item_difficulties - ability_level))

    product = p_right * p_wrong
    information_tensor = np.cumsum(product)
    information = information_tensor[len(information_tensor) - 1]
    return float(information)