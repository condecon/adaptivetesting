from typing import List, Tuple, Literal
import numpy as np
from ...models.__test_item import TestItem, BaseItem, PolyItem
from ...services.__estimator_interface import IEstimator
from .__functions.__estimators import maximize_likelihood_function
from .__test_information import test_information_function
from typing import Sequence


# TODO: introduce switch for estimation depending on the item type
class MLEstimator(IEstimator):
    def __init__(self,
                 response_pattern: List[int] | np.ndarray,
                 items: Sequence[BaseItem],
                 optimization_interval: Tuple[float, float] = (-10, 10),
                 model: Literal["GRM", "GPCM"] | None = None,
                 **kwargs):
        """This class can be used to estimate the current ability level
        of a respondent given the response pattern and the corresponding
        item parameters.
        The estimation uses Maximum Likelihood Estimation.

        Args:
            response_pattern (List[int]): list of response patterns (0: wrong, 1:right)

            items (Sequence[BaseItem]): list of answered items
        """
        IEstimator.__init__(self, response_pattern, items, optimization_interval)

        # decide type of model used
        if isinstance(items, PolyItem):
            self.type: Literal["poly", "dich"] = "poly"
            self.model = model
        else:
            self.type = "dich"

        # ignore additional kwargs
        del kwargs

    def get_estimation(self) -> float:
        """Estimate the current ability level by searching
        for the maximum of the likelihood function.
        A line-search algorithm is used.

        Returns:
            float: ability estimation
        """
        if self.type == "dich":  
            return maximize_likelihood_function(a=self.a,
                                            b=self.b,
                                            c=self.c,
                                            d=self.d,
                                            response_pattern=self.response_pattern,
                                            border=self.optimization_interval)
        if self.type == "poly":
            if self.model == "GRM":
                
    
    def get_standard_error(self, estimation) -> float:
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
            prior=None,
            optimization_interval=self.optimization_interval
        )

        sd_error = 1 / np.sqrt(test_information)
        return float(sd_error)
