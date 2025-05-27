import jax.numpy as jnp
from jax import jit, vmap
from scipy.optimize import minimize_scalar, OptimizeResult # type: ignore
from ....models.__algorithm_exception import AlgorithmException
from ...estimators.__prior import Prior
from scipy.integrate import quad


@jit
def probability_y1(mu: jnp.ndarray,
                   a: jnp.ndarray,
                   b: jnp.ndarray,
                   c: jnp.ndarray,
                   d: jnp.ndarray) -> jnp.ndarray:
    """Probability of getting the item correct given the ability level.

    Args:
        mu (jnp.ndarray): latent ability level
        
        a (jnp.ndarray): item discrimination parameter
        
        b (jnp.ndarray): item difficulty parameter
        
        c (jnp.ndarray): pseudo guessing parameter
        
        d (jnp.ndarray): inattention parameter

    Returns:
        jnp.ndarray: probability of getting the item correct
    """

    value = c + (d - c) * (jnp.exp(a * (mu - b))) / \
        (1 + jnp.exp(a * (mu - b)))
    
    return value


@jit
def probability_y0(mu: jnp.ndarray,
                   a: jnp.ndarray,
                   b: jnp.ndarray,
                   c: jnp.ndarray,
                   d: jnp.ndarray) -> jnp.ndarray:
    """Probability of getting the item wrong given the ability level.

    Args:
            mu (jnp.ndarray): latent ability level
            
            a (jnp.ndarray): item discrimination parameter
            
            b (jnp.ndarray): item difficulty parameter
            
            c (jnp.ndarray): pseudo guessing parameter
            
            d (jnp.ndarray): inattention parameter

    Returns:
        jnp.ndarray: probability of getting the item wrong
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
    For optimization purposes, the function returns the negative value of the likelihood function.
    To get the *real* value, multiply the result by -1.

    Args:
        mu (jnp.ndarray): ability level
        
        a (jnp.ndarray): item discrimination parameter
        
        b (jnp.ndarray): item difficulty parameter
        
        c (jnp.ndarray): pseudo guessing parameter
        
        d (jnp.ndarray): inattention parameter

    Returns:
        float: negative likelihood value of given ability value
    """
    # reshape
    a = jnp.expand_dims(a, axis=0)
    b = jnp.expand_dims(b, axis=0)
    c = jnp.expand_dims(c, axis=0)
    d = jnp.expand_dims(d, axis=0)

    terms = (probability_y1(mu, a, b, c, d)**response_pattern) * \
        (probability_y0(mu, a, b, c, d) ** (1 - response_pattern))
    
    
    return -jnp.prod(terms)


@jit
def posterior(mu: jnp.ndarray,
               a: jnp.ndarray,
               b: jnp.ndarray,
               c: jnp.ndarray,
               d: jnp.ndarray,
               response_pattern: jnp.ndarray,
               prior: Prior | None = None,
               border: tuple[float, float] = (-10, 10)) -> jnp.ndarray:
    """_summary_

    Args:
        a (jnp.ndarray): _description_
        b (jnp.ndarray): _description_
        c (jnp.ndarray): _description_
        d (jnp.ndarray): _description_
        response_pattern (jnp.ndarray): _description_
        prior (Prior | None, optional): _description_. Defaults to None.
        border (tuple[float, float]): _description_. Defaults to (-10, 10).

    Returns:
        jnp.ndarray: _description_
    """
    grid = jnp.linspace(border[0], border[1], 1000)
    def unnormalized(theta):
        like = -likelihood(theta, a, b, c, d, response_pattern)
        if prior:
            return like * prior.pdf(theta)
        return like

    # Vectorize over grid
    unnormalized_vec = vmap(unnormalized)
    values = unnormalized_vec(grid)
    evidence = jnp.trapezoid(values, grid)
    
    return unnormalized(mu) / evidence


@jit
def log_posterior(
               mu: jnp.ndarray,
               a: jnp.ndarray,
               b: jnp.ndarray,
               c: jnp.ndarray,
               d: jnp.ndarray,
               response_pattern: jnp.ndarray,
               prior: Prior | None = None,
               border: tuple[float, float] = (-10, 10),
                ) -> jnp.ndarray:
    """Calculates the log-posterior function.

    Args:
        mu (jnp.ndarray): _description_
        a (jnp.ndarray): _description_
        b (jnp.ndarray): _description_
        c (jnp.ndarray): _description_
        d (jnp.ndarray): _description_
        response_pattern (jnp.ndarray): _description_
        prior (Prior | None, optional): _description_. Defaults to None.
        border (tuple[float, float], optional): _description_. Defaults to (-10, 10).
        num_points (int, optional): _description_. Defaults to 500.

    Returns:
        jnp.ndarray: _description_
    """
    return jnp.log(posterior(
        mu, a, b, c, d, response_pattern, prior, border
    ))




def maximize_likelihood_function(a: jnp.ndarray,
                                 b: jnp.ndarray,
                                 c: jnp.ndarray,
                                 d: jnp.ndarray,
                                 response_pattern: jnp.ndarray,
                                 border: tuple[float, float] = (-10, 10)) -> float:
    """Find the ability value that maximizes the likelihood function.
    This function uses the minimize_scalar function from scipy and the "bounded" method.
    
    Args:
        a (jnp.ndarray): item discrimination parameter
        
        b (jnp.ndarray): item difficulty parameter
        
        c (jnp.ndarray): pseudo guessing parameter
        
        d (jnp.ndarray): inattention parameter

        response_pattern (jnp.ndarray): response pattern of the item
        border (tuple[float, float], optional): border of the optimization interval.
        Defaults to (-10, 10).

    Raises:
        AlgorithmException: if the optimization fails or the response
        pattern consists of only one type of response.

    Returns:
        float: optimized ability value
    """
    # check if response pattern is valid
    if len(set(response_pattern.tolist())) == 1:
        raise AlgorithmException(
            "Response pattern is invalid. It consists of only one type of response.")
    
    result: OptimizeResult = minimize_scalar(likelihood, args=(a, b, c, d, response_pattern),
                                             bounds=border, method='bounded')

    if not result.success:
        raise AlgorithmException(f"Optimization failed: {result.message}")
    else:
        return result.x
