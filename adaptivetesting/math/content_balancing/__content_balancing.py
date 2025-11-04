from abc import ABC, abstractmethod
from ...models.__test_item import TestItem
from ...models.__adaptive_test import AdaptiveTest
from .__constraint import Constraint


class ContentBalancing(ABC):
    def __init__(self, adaptive_test: AdaptiveTest,
                 constraints: list[Constraint]):
        pass

    @abstractmethod
    def select_item(self) -> TestItem | None:
        pass
