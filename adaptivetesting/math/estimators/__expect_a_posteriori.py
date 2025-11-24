import numpy as np
from scipy.integrate import trapezoid
from .__bayes_modal_estimation import BayesModal
from ...models.__test_item import TestItem
from .__functions.__estimators import log_likelihood
from .__prior import Prior
from math import pow


class ExpectedAPosteriori(BayesModal):
    def __init__(self,
                 response_pattern: list[int] | np.ndarray,
                 items: list[TestItem],
                 prior: Prior,
                 optimization_interval: tuple[float, float] = (-10, 10)):
        """This class can be used to estimate the current ability level
            of a respondent given the response pattern and the corresponding
            item difficulties.
            
            This type of estimation finds the mean of the posterior distribution.

            Args:
                response_pattern (List[int] | np.ndarray): list of response patterns (0: wrong, 1:right)

                items (List[TestItem]): list of answered items
            
                prior (Prior): prior distribution

                optimization_interval (Tuple[float, float]): interval used for the optimization function
        """
        super().__init__(response_pattern, items, prior, optimization_interval)

    def get_estimation(self) -> float:
        """Estimate the current ability level using EAP.

        Returns:
            float: ability estimation
        """
        x = np.linspace(self.optimization_interval[0], self.optimization_interval[1], 1000)
        
        if hasattr(self.prior, "logpdf"):
            log_prior = self.prior.logpdf(x)
        else:
            log_prior = np.log(self.prior.pdf(x) + 1e-300)
        
        log_likelihood_vals = np.vectorize(
            lambda mu: log_likelihood(mu,
                                      self.a,
                                      self.b,
                                      self.c,
                                      self.d,
                                      self.response_pattern)
        )(x)
        
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

    def get_standard_error(self, estimated_ability: float) -> float:
        """Calculates the standard error for the items used at the
        construction of the class instance (answered items).
        The currently estimated ability level is required as parameter.

        Args:
            estimated_ability (float): _description_

        Returns:
            float: standard error of the ability estimation
        """
        x = np.linspace(self.optimization_interval[0], self.optimization_interval[1], 1000)
        
        # get log-prior in a numerically stable way
        if hasattr(self.prior, "logpdf"):
            log_prior = self.prior.logpdf(x)
        else:
            log_prior = np.log(self.prior.pdf(x) + 1e-300)
        
        log_likelihood_vals = np.vectorize(lambda mu: log_likelihood(mu,
                                                                     self.a,
                                                                     self.b,
                                                                     self.c,
                                                                     self.d,
                                                                     self.response_pattern))(x)
        log_posterior = log_likelihood_vals + log_prior
        max_log = np.nanmax(log_posterior)
        weights = np.exp(log_posterior - max_log)

        numerator = trapezoid((x - estimated_ability) ** 2 * weights, x)
        
        denominator = trapezoid(weights, x)
        
        standard_error_result = pow(numerator / denominator, 0.5)
    
        return standard_error_result
