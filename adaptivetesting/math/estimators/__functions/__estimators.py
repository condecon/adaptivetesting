import numpy as np
from scipy.optimize import minimize_scalar, OptimizeResult # type: ignore
from ....models.__algorithm_exception import AlgorithmException


def probability_y1(mu: np.ndarray,
                   a: np.ndarray,
                   b: np.ndarray,
                   c: np.ndarray,
                   d: np.ndarray) -> np.ndarray:
    """Probability of getting the item correct given the ability level.

    Args:
        mu (np.ndarray): latent ability level
        a (np.ndarray): item discrimination parameter
        b (np.ndarray): item difficulty parameter
        c (np.ndarray): pseudo guessing parameter
        d (np.ndarray): inattention parameter

    Returns:
        np.ndarray: probability of getting the item correct
    """
    # Compute the exponent safely
    z = a * (mu - b)

    # Use log-sum-exp trick for numerical stability
    # For large positive z: exp(z)/(1+exp(z)) ≈ 1
    # For large negative z: exp(z)/(1+exp(z)) ≈ exp(z)

    # Clip z to prevent overflow in exp()
    z_clipped = np.clip(z, -500, 500)  # exp(-500) and exp(500) are safe

    # Compute the logistic function safely
    # Use different formulas based on the sign of z for stability
    result = np.empty_like(z_clipped)

    # For large positive values, use alternative formula to avoid overflow
    mask_positive = z_clipped > 20  # exp(20) is large but manageable
    mask_negative = z_clipped < -20  # exp(-20) is very small
    mask_medium = ~(mask_positive | mask_negative)

    # Large positive z: 1/(1+exp(-z)) is more stable
    result[mask_positive] = 1.0 / (1.0 + np.exp(-z_clipped[mask_positive]))

    # Large negative z: exp(z)/(1+exp(z)) is stable
    exp_z_neg = np.exp(z_clipped[mask_negative])
    result[mask_negative] = exp_z_neg / (1.0 + exp_z_neg)

    # Medium values: use standard formula
    exp_z_med = np.exp(z_clipped[mask_medium])
    result[mask_medium] = exp_z_med / (1.0 + exp_z_med)

    # Apply the 4PL transformation
    value = c + (d - c) * result

    # Ensure probabilities are within valid range [c, d]
    value = np.clip(value, c, d)

    return np.squeeze(value)


def probability_y0(mu: np.ndarray,
                   a: np.ndarray,
                   b: np.ndarray,
                   c: np.ndarray,
                   d: np.ndarray) -> np.ndarray:
    """Probability of getting the item wrong given the ability level.

    Args:
            mu (np.ndarray): latent ability level

            a (np.ndarray): item discrimination parameter

            b (np.ndarray): item difficulty parameter

            c (np.ndarray): pseudo guessing parameter

            d (np.ndarray): inattention parameter

    Returns:
        np.ndarray: probability of getting the item wrong
    """
    value = 1 - probability_y1(mu, a, b, c, d)
    return value


def likelihood(mu: np.ndarray,
               a: np.ndarray,
               b: np.ndarray,
               c: np.ndarray,
               d: np.ndarray,
               response_pattern: np.ndarray) -> np.ndarray:
    """Likelihood function of the 4-PL model.
    For optimization purposes, the function returns the negative value of the likelihood function.
    To get the *real* value, multiply the result by -1.

    Args:
        mu (np.ndarray): ability level

        a (np.ndarray): item discrimination parameter

        b (np.ndarray): item difficulty parameter

        c (np.ndarray): pseudo guessing parameter

        d (np.ndarray): inattention parameter

    Returns:
        float: negative likelihood value of given ability value
    """
    # reshape
    a = np.expand_dims(a, axis=0)
    b = np.expand_dims(b, axis=0)
    c = np.expand_dims(c, axis=0)
    d = np.expand_dims(d, axis=0)

    terms = (probability_y1(mu, a, b, c, d)**response_pattern) * \
        (probability_y0(mu, a, b, c, d) ** (1 - response_pattern))

    return -np.prod(terms)


def maximize_likelihood_function(a: np.ndarray,
                                 b: np.ndarray,
                                 c: np.ndarray,
                                 d: np.ndarray,
                                 response_pattern: np.ndarray,
                                 border: tuple[float, float] = (-10, 10)) -> float:
    """Find the ability value that maximizes the likelihood function.
    This function uses the minimize_scalar function from scipy and the "bounded" method.

    Args:
        a (np.ndarray): item discrimination parameter

        b (np.ndarray): item difficulty parameter

        c (np.ndarray): pseudo guessing parameter

        d (np.ndarray): inattention parameter

        response_pattern (np.ndarray): response pattern of the item
        border (tuple[float, float], optional): border of the optimization interval.
        Defaults to (-10, 10).

    Raises:
        AlgorithmException: if the optimization fails or the response
        pattern consists of only one type of response.
        AlgorithmException: if the optimization fails or the response
        pattern consists of only one type of response.

    Returns:
        float: optimized ability value
    """
    # check if response pattern is valid
    if len(set(response_pattern.tolist())) == 1:
        raise AlgorithmException(
            "Response pattern is invalid. It consists of only one type of response.")
        raise AlgorithmException(
            "Response pattern is invalid. It consists of only one type of response.")

    result: OptimizeResult = minimize_scalar(likelihood, args=(a, b, c, d, response_pattern),
                                             bounds=border, method='bounded') # type: ignore

    if not result.success:
        raise AlgorithmException(f"Optimization failed: {result.message}")
    else:
        return result.x
