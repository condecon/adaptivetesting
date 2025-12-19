import numpy as np
import numdifftools as nd
from .__poly_math import PolyModelFunctions
from math import log


class GPCM(PolyModelFunctions):
    @staticmethod
    def category_prob(theta: float,
                      a: float,
                      thresholds_list: list[float],
                      response_pattern: int):
        # numerator
        numerator = 0.0
        for i in range(response_pattern):
            # print(f"i: {i}")
            numerator += a * (theta - thresholds_list[i])

        # denominator
        denominator = 1
        possible_categories = len(thresholds_list)
        for c in range(possible_categories):
            local_sum = 0.0
            for i in range(c):
                local_sum += a * (theta - thresholds_list[i])

            denominator += np.exp(local_sum)

        return numerator / denominator
    
    @staticmethod
    def log_likelihood(theta: float,
                       a_params: list[float],
                       thresholds_list: list[list[float]],
                       response_pattern: list[int]):
        log_lik = 0.0
        # Iterate over item indices
        for item_idx in range(len(a_params)):
            prob = GPCM.category_prob(
                theta=theta,
                a=a_params[item_idx],
                thresholds_list=thresholds_list[item_idx],
                response_pattern=response_pattern[item_idx]
            )
            if prob <= 0: # Handle cases where probability is zero or negative
                log_lik += -np.inf # Log of zero is negative infinity
            else:
                log_lik += np.log(prob)
        return -log_lik # Return negative log-likelihood for minimization
    
    @staticmethod
    def fisher_information(theta,
                           a,
                           thresholds,
                           response):
        """Embretson, S. E., & Reise, S. P. (2000). Item Response Theory for Psychologists."""
        def log_prob(x):
            p = GPCM.category_prob(x, a, thresholds, response)
            p = max(p, 1e-12)
            return log(p)
        
        log_prob_d2 = nd.Derivative(log_prob, order=2)
        return -log_prob_d2(theta)
