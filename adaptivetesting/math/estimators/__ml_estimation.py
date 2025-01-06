from typing import List, Tuple
import jax.numpy as np
from ...services.__estimator_interface import IEstimator
from .functions.__estimators import maximize_likelihood_function


class MLEstimator(IEstimator):
    def __init__(self,  
                 response_pattern: List[int] | np.ndarray, 
                 item_difficulties: List[float] | np.ndarray,
                 optimization_interval: Tuple[float, float] = (-10, 10)):
        """This class can be used to estimate the current ability level
        of a respondent given the response pattern and the corresponding
        item difficulties.
        The estimation is based on maximum likelihood estimation and the
        Rasch model.

        Args:
            response_pattern (List[int]): list of response patterns (0: wrong, 1:right)

            item_difficulties (List[float]): list of item difficulties
        """
        IEstimator.__init__(self, response_pattern, item_difficulties, optimization_interval)

    def get_estimation(self) -> float:
        """Estimate the current ability level by searching
        for the maximum of the likelihood function.
        A line-search algorithm is used.

        Returns:
            float: ability estimation
        """
        return maximize_likelihood_function(a=np.array(1),
                                            b=self.item_difficulties,
                                            c=np.array(1),
                                            d=np.array(0),
                                            response_pattern=self.response_pattern,
                                            border=self.optimization_interval)
