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
            response_pattern (List[int]): list of responses (0: wrong, 1:right)
            
            items (List[TestItem]): list of answered items
        """
        if type(response_pattern) is not np.ndarray:
            self.response_pattern = np.array(response_pattern)
        else:
            self.response_pattern = response_pattern
        self.optimization_interval = optimization_interval

        # convert items to parameter arrays
        self.a = np.array([i.a for i in items])
        self.b = np.array([i.b for i in items])
        self.c = np.array([i.c for i in items])
        self.d = np.array([i.d for i in items])
        
    @abstractmethod
    def get_estimation(self) -> float:
        """Get the currently estimated ability.

        Returns:
            float: ability
        """
        pass
