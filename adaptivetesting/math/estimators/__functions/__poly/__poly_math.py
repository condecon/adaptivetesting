from abc import ABC, abstractmethod
from scipy.optimize import minimize_scalar, OptimizeResult
from .....models.__algorithm_exception import AlgorithmException
from ...__prior import Prior
import numpy as np
from scipy.integrate import trapezoid


class PolyModelFunctions(ABC):
    

    @staticmethod
    @abstractmethod
    def category_prob(theta: float,
                      a: float,
                      thresholds_list: list[float],
                      response_pattern: int):
        pass

    @staticmethod
    @abstractmethod
    def log_likelihood(theta: float,
                       a_params: list[float],
                       thresholds_list: list[list[float]],
                       response_pattern: list[int]):
        pass
    
    @staticmethod
    @abstractmethod
    def fisher_information(theta: float,
                           a: float,
                           thresholds: list[float]):
        pass
    
    def maximize_likelihood_function(self,
                                     a_params: list[float],
                                     thresholds_list: list[list[float]],
                                     response_pattern: list[int],
                                     border: tuple[float, float] = (-10, 10)):

        result: OptimizeResult = minimize_scalar(lambda mu: -self.log_likelihood(mu,
                                                                                 a_params,
                                                                                 thresholds_list,
                                                                                 response_pattern),
                                                 bounds=border,
                                                 method='bounded')

        if not result.success:
            raise AlgorithmException(f"Optimization failed: {result.message}")
        else:
            return result.x
        
    def maximize_posterior(self,
                           a_params: list[float],
                           thresholds_list: list[list[float]],
                           response_pattern: list[int],
                           prior: Prior,
                           optimization_interval: tuple[float, float] = (-10, 10)
                           ) -> float:
        
        def log_posterior(mu):
            log_likelihood_res = np.array(self.log_likelihood(mu,
                                                              a_params,
                                                              thresholds_list,
                                                              response_pattern))

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

    def posterior_mean(self,
                       a_params: list[float],
                       thresholds_list: list[list[float]],
                       response_pattern: list[int],
                       prior: Prior,
                       optimization_interval: tuple[float, float] = (-10, 10)) -> float:
        x = np.linspace(optimization_interval[0], optimization_interval[1], 1000)

        if hasattr(prior, "logpdf"):
            log_prior = prior.logpdf(x)
        else:
            log_prior = np.log(prior.pdf(x) + 1e-300)
        
        log_likelihood_vec = np.vectorize(
            lambda mu: self.log_likelihood(mu, a_params, thresholds_list, response_pattern)
        )

        log_likelihood_vals = log_likelihood_vec(x)

        log_posterior = log_likelihood_vals + log_prior

        # use log-sum-exp stabilization
        max_log = np.nanmax(log_posterior)
        weights = np.exp(log_posterior - max_log)

        numerator = trapezoid(x * weights, x)
        denominator = trapezoid(weights, x) + np.finfo(float).eps

        if denominator == 0 or not np.isfinite(denominator):
            raise ValueError("Denominator (integral of posterior) is zero or "
                             "non-finite — check interval/prior/likelihood.")

        estimation = numerator / denominator
        return estimation
