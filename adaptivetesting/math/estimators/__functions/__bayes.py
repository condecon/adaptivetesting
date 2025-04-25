import jax.numpy as np
from scipy.optimize import minimize_scalar, OptimizeResult # type: ignore
from .__estimators import likelihood
from ..__prior import Prior
from ....models.__algorithm_exception import AlgorithmException


def maximize_posterior(
    a: np.ndarray,
    b: np.ndarray,
    c: np.ndarray,
    d: np.ndarray,
    response_pattern: np.ndarray,
    prior: Prior
) -> float:
    """_summary_

    Args:
        a (np.ndarray): _description_
        
        b (np.ndarray): _description_
        
        c (np.ndarray): _description_
        
        d (np.ndarray): _description_
        
        response_pattern (np.ndarray): _description_
        
        prior (Prior): _description_

    Returns:
        float: Bayes Modal estimator for the given parameters
    """
    def posterior(mu) -> np.ndarray:
        return likelihood(mu, a, b, c, d, response_pattern) * prior.pdf(mu)
    
    result: OptimizeResult = minimize_scalar(lambda mu: posterior(mu),
                                             bounds=(-10, 10),
                                             method="bounded") # type: ignore
    
    if not result.success:
        raise AlgorithmException(f"Optimization failed: {result.message}")
    
    else:
        return float(result.x)
