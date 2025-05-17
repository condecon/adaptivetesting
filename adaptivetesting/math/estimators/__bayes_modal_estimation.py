from typing import List, Tuple
import jax.numpy as np
from ...services.__estimator_interface import IEstimator
from ...models.__test_item import TestItem
from ...models.__algorithm_exception import AlgorithmException
from .__functions.__bayes import maximize_posterior, likelihood
from .__prior import Prior, NormalPrior


class BayesModal(IEstimator):
    def __init__(self,
                 response_pattern: List[int] | np.ndarray,
                 items: List[TestItem],
                 prior: Prior,
                 optimization_interval: Tuple[float, float] = (-10, 10)):
        """This class can be used to estimate the current ability level
            of a respondent given the response pattern and the corresponding
            item difficulties.
            
            This type of estimation finds the maximum of the posterior distribution.


            Args:
                response_pattern (List[int] | np.ndarray ): list of response patterns (0: wrong, 1:right)

                items (List[TestItem]): list of answered items
            
                prior (Prior): prior distribution

                optimization_interval (Tuple[float, float]): interval used for the optimization function
            """
        super().__init__(response_pattern, items, optimization_interval)

        self.prior = prior

    def get_estimation(self) -> float:
        """Estimate the current ability level using Bayes Modal.

        Raises:
            AlgorithmException: Raised when maximum could not be found.
        
        Returns:
            float: ability estimation
        """
        if isinstance(self.prior, NormalPrior):
            # get estimate using a classical optimizers approach
            return maximize_posterior(
                self.a,
                self.b,
                self.c,
                self.d,
                self.response_pattern,
                self.prior
            )
        # else, we have to calculate the full posterior distribution
        # because the optimizers do not correctly identify the maximum of the function
        else:
            mu = np.linspace(self.optimization_interval[0],
                             self.optimization_interval[1],
                             num=1000)
            # calculate likelihood values for every mu
            try:
                lik_values = np.array([
                    likelihood(
                        i,
                        self.a,
                        self.b,
                        self.c,
                        self.d,
                        self.response_pattern
                    )
                    for i in mu
                ])

                # add prior
                unmarginalized_posterior = lik_values * self.prior.pdf(mu)
                # find argmax and return mu
                estimate_index = np.argmax(unmarginalized_posterior)
                return float(mu[estimate_index].astype(float))
            except Exception as e:
                raise AlgorithmException(e)

    def get_standard_error(self, estimation: float) -> float:

        # check for prior
        if isinstance(self.prior, NormalPrior):
            pass
        else:
            pass

        raise NotImplementedError()
