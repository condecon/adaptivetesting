import numpy as np
from scipy.integrate import trapezoid
from .__bayes_modal_estimation import BayesModal
from ...models.__test_item import TestItem
from .__functions.__bayes import likelihood
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
        
        prior_pdf = self.prior.pdf(x)
        
        likelihood_vals = np.vectorize(lambda mu: likelihood(mu,
                                                             self.a,
                                                             self.b,
                                                             self.c,
                                                             self.d,
                                                             self.response_pattern))(x)
        
        numerator = trapezoid(x * likelihood_vals * prior_pdf, x)
        
        denominator = trapezoid(likelihood_vals * prior_pdf, x)
        
        estimation = numerator / denominator
        
        return estimation

    def get_standard_error(self, estimated_ability: float) -> float:
        """Calculates the standard error for the items used at the
        construction of the class instance (answered items).
        The currently estimated ability level is required as parameter.

        Args:
            estimated_ability (float): _description_

        Raises:
            NotImplementedError: Either an instance of NormalPrior or CustomPrior has to be used.
                                 If you want to use another calculation method for the standard,
                                 you have to specifically override this method.

        Returns:
            float: standard error of the ability estimation
        """
        x = np.linspace(self.optimization_interval[0], self.optimization_interval[1], 1000)
        prior_pdf = self.prior.pdf(x)
        
        likelihood_vals = np.vectorize(lambda mu: likelihood(mu,
                                                             self.a,
                                                             self.b,
                                                             self.c,
                                                             self.d,
                                                             self.response_pattern))(x)
        
        numerator = trapezoid((x - estimated_ability) ** 2 * likelihood_vals * prior_pdf, x)
        
        denominator = trapezoid(likelihood_vals * prior_pdf, x)
        
        standard_error_result = pow(numerator / denominator, 0.5)
    
        return standard_error_result
