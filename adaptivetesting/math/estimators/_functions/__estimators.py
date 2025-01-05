import jax.numpy as jnp
from jax import jit
from scipy.optimize import minimize_scalar, OptimizeResult # type: ignore
from adaptivetesting.models.algorithm_exception import AlgorithmException

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
        float: log-likelihood value of given ability value
    """
    value = c + (d - c) * \
        (jnp.exp(a * response_pattern * (mu - b))) / \
        (1 + jnp.exp(a * (mu - b)))
    
    return -jnp.cumulative_prod(value)[-1].astype(float)

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
    result: OptimizeResult = minimize_scalar(likelihood, args=(a, b, c, d, response_pattern), bounds=border, method='bounded')

    if not result.success:
        raise AlgorithmException(f"Optimization failed: {result.message}")
    else:
        return result.x
   