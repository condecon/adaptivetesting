import numpy as np
from math import log
from scipy.integrate import quad
import numdifftools as nd
from .__poly_math import PolyModelFunctions


class GRM(PolyModelFunctions):
    @staticmethod
    def category_prob(theta, a: float, thresholds: list[float], k: int):
        # k is the category index (0, 1, ..., num_thresholds)
        num_thresholds = len(thresholds)

        # Calculate P(Y >= k)
        if k == 0:
            p_ge_k = 1.0
        elif k > 0 and k <= num_thresholds:
            p_ge_k = 1 / (1 + np.exp(-a * (theta - thresholds[k-1])))
        else:
            # Invalid category index k or k > num_categories (num_thresholds + 1)
            # For likelihood calculation, return a very small positive number to avoid log(0)
            # Ensure the returned type matches the expected type if theta was an array
            return np.full_like(theta, 1e-10, dtype=float) if isinstance(theta, np.ndarray) else 1e-10

        # Calculate P(Y >= k+1)
        if k == num_thresholds: # k+1 would correspond to P(Y >= num_thresholds + 1) which is 0.0
            p_ge_k_plus_1 = 0.0
        elif k < num_thresholds: # k+1 is <= num_thresholds, so it uses thresholds[k]
            p_ge_k_plus_1 = 1 / (1 + np.exp(-a * (theta - thresholds[k])))
        else:
            # Invalid k+1 (should not be less than 0 or something)
            # Ensure the returned type matches the expected type if theta was an array
            return np.full_like(theta, 1e-10, dtype=float) if isinstance(theta, np.ndarray) else 1e-10

        prob_k = p_ge_k - p_ge_k_plus_1
        return np.maximum(prob_k, 1e-10) # Use np.maximum for element-wise comparison with arrays
    
    @staticmethod
    def log_likelihood(theta: float, a_params: list[float], thresholds_list: list[list[float]], response_pattern: list[int]):
        log_lik = 0.0
        # Iterate over item indices
        for item_idx in range(len(a_params)):
            prob = GRM.category_prob(
                theta=theta,
                a=a_params[item_idx],
                thresholds=thresholds_list[item_idx],
                k=response_pattern[item_idx]
            )
            if prob <= 0: # Handle cases where probability is zero or negative
                log_lik += -np.inf # Log of zero is negative infinity
            else:
                log_lik += np.log(prob)
        return -log_lik # Return negative log-likelihood for minimization
    
    @staticmethod
    def fisher_information(theta: float,
                           a: float,
                           thresholds: list[float],
                           response: int):
        """Embretson, S. E., & Reise, S. P. (2000). Item Response Theory for Psychologists."""
        def log_prob(x):
            p = GRM.category_prob(x, a, thresholds, response)
            p = max(p, 1e-12)
            return log(p)

        log_prob_d2 = nd.Derivative(log_prob, order=2)
        return -log_prob_d2(theta)