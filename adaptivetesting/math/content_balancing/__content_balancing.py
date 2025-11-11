from abc import ABC, abstractmethod
from ...models.__test_item import TestItem
from ...models.__adaptive_test import AdaptiveTest
from .__constraint import Constraint
from typing import Literal


type CONTENT_BALANCING = Literal["WeightedPenaltyModel", "MaximumPriorityIndex"]
"""Default available content balancing methods."""

class ContentBalancing(ABC):
    """Abstract base class for content balancing methods.

    Abstract Methods
    ------------------
    - `select_item`
    """
    def __init__(self, adaptive_test: AdaptiveTest,
                 constraints: list[Constraint]):
        """
        Args:
            adaptive_test (AdaptiveTest): instance of the adaptive test
            constraints (list[Constraint]): constraints that are applied to the item selection
        """
        pass

    @abstractmethod
    def select_item(self) -> TestItem | None:
        """Select an item based on the implemented selection rules

        Returns:
            TestItem | None: selected test item
        """
        pass
