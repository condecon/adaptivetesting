from typing import List, Tuple
import numpy as np
from ...services.__estimator_interface import IEstimator
from ...models.__test_item import TestItem
from ...models.__algorithm_exception import AlgorithmException
from .__functions.__bayes import maximize_posterior, likelihood
from .__prior import Prior, NormalPrior, CustomPrior, CustomPriorException
from .__test_information import test_information_function


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
        If a `NormalPrior` is used, the `bounded` optimizer is used
        to get the ability estimate.
        For any other prior, it cannot be guaranteed that the optimizer will converge correctly.
        Therefore, the full posterior distribution is calculated
        and the maximum posterior value is selected.

        Because this function uses a switch internally to determine
        whether a optimizer is used for the estimate or not,
        you have to create your custom priors from the correct base class (`CustomPrior`).
        Otherwise, the estimate may not necessarily be correct!

        Raises:
            AlgorithmException: Raised when maximum could not be found.
            CustomPriorException: Raised when custom prior is not based on the `CustomPrior` class.
        
        Returns:
            float: ability estimation
        """
        if type(self.prior) is NormalPrior:
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
            # check that the used prior is really inherited from
            # the CustomPrior base class
            if not isinstance(self.prior, CustomPrior):
                raise CustomPriorException("It seems like you are using a non-normal prior but",
                                           "did not use the CustomPrior base class!")
            
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
                # find argmin and return mu
                estimate_index = np.argmin(unmarginalized_posterior)
                return float(mu[estimate_index].astype(float))
            except Exception as e:
                raise AlgorithmException(e)

    def get_standard_error(self, estimation: float) -> float:
        """Calculates the standard error for the given estimated ability level.

        Args:
            estimation (float): currently estimated ability level

        Returns:
            float: standard error of the ability estimation
        """
        test_information = test_information_function(
            np.array(estimation, dtype=float),
            a=self.a,
            b=self.b,
            c=self.c,
            d=self.d,
            prior=self.prior,
            optimization_interval=self.optimization_interval
        )

        sd_error = 1 / np.sqrt(test_information)
        return float(sd_error)
