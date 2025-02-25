import jax.numpy as np
from jax import jit
from scipy.optimize import minimize_scalar, OptimizeResult # type: ignore
from scipy.integrate import quad
from .__estimators import likelihood
from ..__priors import Prior
from ....models.__algorithm_exception import AlgorithmException


jit
def p_data(x: np.ndarray, a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray, response_pattern: np.ndarray, prior: Prior):
    integrand = lambda mu: likelihood(mu, a, b, c, d, response_pattern) * prior.pdf(mu)
    result, _ = quad(integrand, -np.inf, np.inf)
    return result

def maximize_posterior(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray, response_pattern: np.ndarray, prior: Prior):
    posterior = lambda mu: likelihood(mu, a, b, c, d, response_pattern) * prior.pdf(mu) / p_data(mu, a, b, c, d, response_pattern, prior)
    result: OptimizeResult = minimize_scalar(lambda mu: -posterior(mu), bounds=(-10, 10), method='bounded')
    
    if not result.success:
        raise AlgorithmException(f"Optimization failed: {result.message}")
    else:
        return result.x  