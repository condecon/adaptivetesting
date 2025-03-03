import jax.numpy as jnp
from jax import jit
from scipy.optimize import minimize_scalar, OptimizeResult # type: ignore
from ....models.__algorithm_exception import AlgorithmException

@jit
def probability_y1(mu: jnp.ndarray,
               a: jnp.ndarray, 
               b: jnp.ndarray, 
               c: jnp.ndarray, 
               d: jnp.ndarray) -> jnp.ndarray:
    """_summary_

    Args:
        mu (jnp.ndarray): _description_
        a (jnp.ndarray): _description_
        b (jnp.ndarray): _description_
        c (jnp.ndarray): _description_
        d (jnp.ndarray): _description_

    Returns:
        jnp.ndarray: _description_
    """

    value = c + (d-c) * (jnp.exp(a * (mu - b)))/ \
        (1 + jnp.exp(a * (mu - b)))
    
    return value

@jit
def probability_y0(mu: jnp.ndarray,
               a: jnp.ndarray, 
               b: jnp.ndarray, 
               c: jnp.ndarray, 
               d: jnp.ndarray) -> jnp.ndarray:
    """_summary_

    Args:
        mu (jnp.ndarray): _description_
        a (jnp.ndarray): _description_
        b (jnp.ndarray): _description_
        c (jnp.ndarray): _description_
        d (jnp.ndarray): _description_

    Raises:
        AlgorithmException: _description_
        AlgorithmException: _description_

    Returns:
        jnp.ndarray: _description_
    """
    value = 1 - probability_y1(mu, a, b, c, d)
    return value

@jit
def likelihood(mu: jnp.ndarray,
               a: jnp.ndarray, 
               b: jnp.ndarray, 
               c: jnp.ndarray, 
               d: jnp.ndarray, 
               response_pattern: jnp.ndarray) -> jnp.ndarray:
    """Likelihood function of the 4-PL model.
    To get the * real * value, multiply the result by -1.

    Args:
        mu (jnp.ndarray): ability level
        a (jnp.ndarray): discrimination parameter
        b (jnp.ndarray): difficulty parameter
        c (jnp.ndarray): guessing parameter
        d (jnp.ndarray): slipping parameter

    Returns:
        float: likelihood value of given ability value
    """
    terms = (probability_y1(mu, a, b, c, d)**response_pattern) * (probability_y0(mu, a, b, c, d) ** (1 - response_pattern))
    
    return -jnp.cumulative_prod(terms)[-1].astype(float)

def maximize_likelihood_function(a: jnp.ndarray, 
                                 b: jnp.ndarray, 
                                 c: jnp.ndarray, 
                                 d: jnp.ndarray, 
                                 response_pattern: jnp.ndarray,
                                 border: tuple[float, float] = (-10, 10)) -> float:
    """Maximize the likelihood function using scipy's minimize_scalar.
    
    Args:
        mu (jnp.ndarray): ability level
        a (jnp.ndarray): discrimination parameter
        b (jnp.ndarray): difficulty parameter
        c (jnp.ndarray): guessing parameter
        d (jnp.ndarray): slipping parameter

        response_pattern (jnp.ndarray): response pattern of the item
        border (tuple[float, float], optional): border of the optimization. Defaults to (-10, 10).

    Returns:
        float: optimized ability value
    """
    # check if response pattern is valid
    if len(set(response_pattern.tolist())) == 1:
        raise AlgorithmException("Response pattern is invalid. It consists of only one type of response.")
    
    
    result: OptimizeResult = minimize_scalar(likelihood, args=(a, b, c, d, response_pattern), bounds=border, method='bounded')

    if not result.success:
        raise AlgorithmException(f"Optimization failed: {result.message}")
    else:
        return result.x
   