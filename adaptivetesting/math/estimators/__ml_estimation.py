from typing import List, Tuple
import jax.numpy as np
from ...models.__test_item import TestItem
from ...services.__estimator_interface import IEstimator
from .__functions.__estimators import maximize_likelihood_function


class MLEstimator(IEstimator):
    def __init__(self,
                 response_pattern: List[int] | np.ndarray,
                 items: List[TestItem],
                 optimization_interval: Tuple[float, float] = (-10, 10)):
        """This class can be used to estimate the current ability level
        of a respondent given the response pattern and the corresponding
        item parameters.
        The estimation uses Maximum Likelihood Estimation.

        Args:
            response_pattern (List[int]): list of response patterns (0: wrong, 1:right)

            items (List[TestItem]): list of answered items
        """
        IEstimator.__init__(self, response_pattern, items, optimization_interval)

    def get_estimation(self) -> float:
        """Estimate the current ability level by searching
        for the maximum of the likelihood function.
        A line-search algorithm is used.

        Returns:
            float: ability estimation
        """
        
        return maximize_likelihood_function(a=self.a,
                                            b=self.b,
                                            c=self.c,
                                            d=self.d,
                                            response_pattern=self.response_pattern,
                                            border=self.optimization_interval)
