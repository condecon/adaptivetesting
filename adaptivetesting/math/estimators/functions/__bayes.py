import numpy as np
from scipy.optimize import minimize_scalar, OptimizeResult # type: ignore
from ..__prior import Prior
from ....models.__algorithm_exception import AlgorithmException
from .__estimators import log_likelihood


def maximize_posterior(
    a: np.ndarray,
    b: np.ndarray,
    c: np.ndarray,
    d: np.ndarray,
    response_pattern: np.ndarray,
    prior: Prior,
    optimization_interval: tuple[float, float] = (-10, 10)
) -> float:
    """Get the maximum of the posterior distribution

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
    def log_posterior(mu):
        log_likelihood_res = log_likelihood(mu, a, b, c, d, response_pattern)

        if hasattr(prior, "logpdf"):
            log_prior = prior.logpdf(mu)
        else:
            log_prior = np.log(np.clip(prior.pdf(mu), 1e-300, None))
    
        log_post = log_likelihood_res + log_prior

        if not np.isfinite(log_post):
            return -1e300
        else:
            return float(log_post.ravel()[0])
    
    result: OptimizeResult = minimize_scalar(lambda mu: -log_posterior(mu),
                                             bounds=optimization_interval,
                                             method="bounded") # type: ignore
    
    if not result.success:
        raise AlgorithmException(f"Optimization failed: {result.message}")
    
    else:
        return float(result.x)
