import numpy as np
from scipy.special import logsumexp
import numdifftools as nd
import math
from .__poly_math import PolyModelFunctions


class GPCM(PolyModelFunctions):
    @staticmethod
    def category_prob(theta: float,
                      a: float,
                      thresholds_list: list[float],
                      response_pattern: int):
        m = len(thresholds_list)

        # Compute eta_k values (log numerators)
        etas = np.zeros(m + 1)

        for k in range(1, m + 1):
            etas[k] = etas[k - 1] + a * (theta - thresholds_list[k - 1])

        # Compute log denominator safely
        log_denom = logsumexp(etas)

        # log probability
        log_prob = etas[response_pattern] - log_denom

        return log_prob
    
    @staticmethod
    def log_likelihood(theta: float,
                       a_params: list[float],
                       thresholds_list: list[list[float]],
                       response_pattern: list[int]):
        log_lik = 0.0
        # Iterate over item indices
        for item_idx in range(len(a_params)):
            log_prob = GPCM.category_prob(
                theta=theta,
                a=a_params[item_idx],
                thresholds_list=thresholds_list[item_idx],
                response_pattern=response_pattern[item_idx]
            )
            
            log_lik += log_prob
        return log_lik # Return negative log-likelihood for minimization
    
    @staticmethod
    def fisher_information(theta: float,
                           a: float,
                           thresholds: list[float]):
        """Embretson, S. E., & Reise, S. P. (2000). Item Response Theory for Psychologists.
        p. 185
        primary citation Dodd, DeAyala & Koch 1995
        """
        def prob(x: float, category: int):
            p = math.exp(GPCM.category_prob(x, a, thresholds, category))
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
