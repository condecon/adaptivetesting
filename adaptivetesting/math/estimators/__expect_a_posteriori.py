import jax.numpy as np
from scipy.integrate import quad
from .__bayes_modal_estimation import BayesModal
from ...models.__test_item import TestItem
from .__functions.__bayes import likelihood
from .__prior import Prior


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
        """Estimate the crrent ability level using EAP.

        Returns:
            float: ability estimation
        """
        integral_likelihood_times_prior_times_mu, _ = quad(lambda mu: mu * likelihood(
            mu, self.a, self.b, self.c, self.d, self.response_pattern
        ) * self.prior.pdf(mu),
        a=self.optimization_interval[0],
        b=self.optimization_interval[1])


        integral_likelihood_times_prior, _ = quad(lambda mu: likelihood(
            mu, self.a, self.b, self.c, self.d, self.response_pattern
        ) * self.prior.pdf(mu),
        a=self.optimization_interval[0],
        b=self.optimization_interval[1])

        estimation = integral_likelihood_times_prior_times_mu / integral_likelihood_times_prior
        return estimation
