from abc import ABC, abstractmethod
from typing import Literal
from ... import TestItem
from ...models.__adaptive_test import AdaptiveTest


type EXPOSURECONTROL = Literal["Randomesque"]

class ExposureControl(ABC):
    """
    Abstract base class for exposure control

    Abstract Methods
    ------------------
    - `select_item`
    """
    def __init__(self, adaptive_test: AdaptiveTest):
        """
        Args:
            adaptive_test (AdaptiveTest): instance of the adaptive test
        """
        self.adaptive_test = adaptive_test

    @abstractmethod
    def select_item(self, **kwargs) -> TestItem:
        """Select an item based on the implemented selection rules

                Returns:
                    TestItem | None: selected test item
        """
        pass