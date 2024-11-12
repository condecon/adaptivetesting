from abc import ABC, abstractmethod
from typing import List
import numpy as np

class IEstimator(ABC):
    def __init__(self,
                 response_pattern: List[int],
                 item_difficulties: List[float]):
        """This is the interface required for every possible
        estimator.
        Any estimator inherits from this class and implements
        the `get_estimation` method.

        Args:
            response_pattern (List[int]): list of responses (0: wrong, 1:right)
            item_difficulties (List[float]): list of item difficulties
        """
        self.response_pattern = np.array(response_pattern)
        self.item_difficulties = np.array(item_difficulties)

    @abstractmethod
    def get_estimation(self) -> float:
        """Get the currently estimated ability.

        Returns:
            float: ability
        """
        pass
