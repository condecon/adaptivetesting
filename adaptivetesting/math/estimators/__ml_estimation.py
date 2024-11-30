from typing import List
import numpy as np
from scipy.optimize import minimize, OptimizeResult, Bounds
from ...models.__algorithm_exception import AlgorithmException
from ...services.__estimator_interface import IEstimator


class MLEstimator(IEstimator):
    def __init__(self, response_pattern: List[int], item_difficulties: List[float]):
        """This class can be used to estimate the current ability level
        of a respondent given the response pattern and the corresponding
        item difficulties.
        The estimation is based on maximum likelihood estimation and the
        Rasch model.

        Args:
            response_pattern (List[int]): list of response patterns (0: wrong, 1:right)

            item_difficulties (List[float]): list of item difficulties
        """
        self.response_pattern = np.array(response_pattern)
        self.item_difficulties = np.array(item_difficulties)

    def get_estimation(self) -> float:
        """Estimate the current ability level by searching
        for the maximum of the likelihood function.
        A line-search algorithm is used.

        Returns:
            float: ability estimation
        """
        return self._find_max()

    def likelihood(self, ability: np.ndarray) -> float:
        """First derivative of the log-likelihood function.

        Args:
            ability (np.ndarray): ability level

        Returns:
            float: log-likelihood value of given ability value
        """
        mu_T = ability[..., None]

        item_term_up = np.exp(self.response_pattern * (mu_T - self.item_difficulties))
        item_term_down = 1 + np.exp(mu_T - self.item_difficulties)
        item_term = item_term_up / item_term_down

        cumprod = np.cumprod(item_term, axis=1)[:, -1]
        return -cumprod

    def _find_max(self) -> float:
        """
        Starts gradient descent algorithm.
        Do not call directly.
        Instead, use get_maximum_likelihood_estimation.

        Returns:
            float: ability estimation

        Raises:
            AlgorithmException
        """
        result: OptimizeResult = minimize(self.likelihood,
                                          x0=np.array([-10]),
                                          method="L-BFGS-B")
        if result.success == False:
            raise AlgorithmException("Algorithm did not converge!")
        
        x_float: float = result.x.astype(float)[0]
        if x_float < -10:
            raise AlgorithmException("Algorithm did not converge correctly!")
        else:
            return result.x.astype(float)[0]
        