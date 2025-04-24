from typing import List, Tuple
import jax.numpy as np
from ...services.__estimator_interface import IEstimator
from ...models.__test_item import TestItem
from .__functions.__bayes import maximize_posterior
from .__prior import Prior


class BayesModal(IEstimator):
    def __init__(self,
                 response_pattern: List[int] | np.ndarray,
                 items: List[TestItem],
                 prior: Prior,
                 optimization_interval: Tuple[float, float] = (-10, 10)):
        """This class can be used to estimate the current ability level
            of a respondent given the response pattern and the corresponding
            item difficulties.
            The estimation is based on maximum likelihood estimation and the
            Rasch model.

            Args:
                response_pattern (List[int]): list of response patterns (0: wrong, 1:right)

                items (List[TestItem]): list of answered items
            
                prior (Prior): prior distribution
            """
        super().__init__(response_pattern, items, optimization_interval)

        self.prior = prior

    def get_estimation(self) -> float:
        """Estimate the current ability level using Bayes Modal.
        
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
