from abc import ABC, abstractmethod
from typing import List, Tuple
import jax.numpy as np
from ..models.__test_item import TestItem

class IEstimator(ABC):
    def __init__(self,  
                 response_pattern: List[int] | np.ndarray, 
                 items: List[TestItem],
                 optimization_interval: Tuple[float, float] = (-10, 10)):
        """This is the interface required for every possible
        estimator.
        Any estimator inherits from this class and implements
        the `get_estimation` method.

        Args:
            response_pattern (List[int]): list of response patterns (0: wrong, 1:right)

            items (List[TestItem]): list of items
        """
        if type(response_pattern) is not np.ndarray:
            self.response_pattern = np.array(response_pattern)
        else:
            self.response_pattern = response_pattern

        self.items = items

        self.optimization_interval = optimization_interval
        
    @abstractmethod
    def get_estimation(self) -> float:
        """Get the currently estimated ability.

        Returns:
            float: ability
        """
        pass
