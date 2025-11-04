import numpy as np
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
    prior: Prior,
    optimization_interval: tuple[float, float] = (-10, 10)
) -> float:
    """_summary_

    Args:
        a (np.ndarray): item parameter a
    
        b (np.ndarray): item parameter b
        
        c (np.ndarray): item parameter c
        
        d (np.ndarray): item parameter d
        
        response_pattern (np.ndarray): response pattern (simulated or user generated)
        
        prior (Prior): prior distribution

        optimization_interval (Tuple[float, float]): interval used for the optimization function

    Returns:
        float: Bayes Modal estimator for the given parameters
    """
    def posterior(mu) -> np.ndarray:
        return likelihood(mu, a, b, c, d, response_pattern) * prior.pdf(mu)
    
    result: OptimizeResult = minimize_scalar(lambda mu: posterior(mu),
                                             bounds=optimization_interval,
                                             method="bounded") # type: ignore
    
    if not result.success:
        raise AlgorithmException(f"Optimization failed: {result.message}")
    
    else:
        return float(result.x)
