import numpy as np
import numdifftools as nd
from .__poly_math import PolyModelFunctions


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
    def fisher_information(theta: float,
                           a: float,
                           thresholds: list[float]):
        """Embretson, S. E., & Reise, S. P. (2000). Item Response Theory for Psychologists.
        p. 185
        primary citation Dodd, DeAyala & Koch 1995
        """
        def prob(x: float, category: int):
            p = GPCM.category_prob(x, a, thresholds, category)
            p = max(p, 1e-12)
            return p
        prob_d1 = nd.Derivative(prob, order=1)
        
        def category_information(x: float, category: int):
            cat_inf = (prob_d1(x, category) ** 2) / prob(x, category)
            return cat_inf
        
        item_inf = 0
        for cat in range(len(thresholds) + 1):
            item_inf = item_inf + category_information(theta, cat)

        return item_inf
