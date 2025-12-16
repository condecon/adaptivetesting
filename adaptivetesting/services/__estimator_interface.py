from abc import ABC, abstractmethod
from typing import List, Tuple, cast, Sequence
import numpy as np
from ..models.__test_item import TestItem, BaseItem, PolyItem


class IEstimator(ABC):
    def __init__(self,
                 response_pattern: List[int] | np.ndarray,
                 items: List[BaseItem],
                 optimization_interval: Tuple[float, float] = (-10, 10)):
        """This is the interface required for every possible
        estimator.
        Any estimator inherits from this class and implements
        the `get_estimation` method.

        Args:
            response_pattern (List[int]): list of responses (0: wrong, 1:right)
            items (List[BaseItem]): list of answered items
        """
        if type(response_pattern) is not np.ndarray:
            self.response_pattern = np.array(response_pattern)
        else:
            self.response_pattern = response_pattern
        self.optimization_interval = optimization_interval

        if isinstance(items[0], TestItem):
            # convert items to parameter arrays
            items_t = cast(list[TestItem], items)
            self.a = np.array([i.a for i in items_t])
            self.b = np.array([i.b for i in items_t])
            self.c = np.array([i.c for i in items_t])
            self.d = np.array([i.d for i in items_t])

        if isinstance(items[0], PolyItem):
            items_tp = cast(list[PolyItem], items)
            self.a_params = [i.a for i in items_tp]
            self.thresholds_list: list[list[float]] = [i.b for i in items_tp]
        
    @abstractmethod
    def get_estimation(self) -> float:
        """Get the currently estimated ability.

        Returns:
            float: ability
        """
        pass

    @abstractmethod
    def get_standard_error(self, estimation: float) -> float:
        """Calculates the standard error for the given estimated ability level.

        Args:
            estimation (float): currently estimated ability level

        Returns:
            float: standard error of the ability estimation
        """
        pass
