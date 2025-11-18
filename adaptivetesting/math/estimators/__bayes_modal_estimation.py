from typing import List, Tuple
import numpy as np
from ...services.__estimator_interface import IEstimator
from ...models.__test_item import TestItem
from ...models.__algorithm_exception import AlgorithmException
from .__functions.__bayes import maximize_posterior
from .__functions.__estimators import likelihood
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
        The `bounded` optimizer is used
        to get the ability estimate.
        
        Raises:
            AlgorithmException: Raised when maximum could not be found.
        
        Returns:
            float: ability estimation
        """
       
        return maximize_posterior(
            self.a,
            self.b,
            self.c,
            self.d,
            self.response_pattern,
            self.prior
        )

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
