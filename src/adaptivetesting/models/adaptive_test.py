from typing import List
from .test_item import TestItem
from ..math.urrys_rule import urrys_rule
from ..math.standard_error import standard_error
import abc
from .test_result import TestResult
from ..data.sqlite_context import SQLiteContext

class AdaptiveTest(abc.ABC):
    """Abstract class of adaptive test.
    All abstract methods have to be overriden
    to create an instance of this class.

    Abstract methods:
        - estimate_ability_level
    """
    def __init__(self, items: List[TestItem],
                 simulation_id: str,
                 participant_id: int,
                 true_ability_level: float,
                 initial_ability_level: float = 0,
                 DEBUG=False):
        self.true_ability_level: float = true_ability_level
        self.simulation_id = simulation_id
        self.participant_id: int = participant_id
        # set start values
        self.ability_level = initial_ability_level
        self.answered_items: List[TestItem] = []
        self.response_pattern: List[int] = []
        self.test_results: List[TestResult] = []
        # load items
        self.items = items

        # debug
        self.DEBUG = DEBUG

        # data context
        self.data_context = SQLiteContext(simulation_id, participant_id)

    def get_item_difficulties(self) -> List[float]:
        """Return difficulties of items in item pool."""
        return [item.b for item in self.items]

    def get_answered_items_difficulties(self) -> List[float]:
        """Returns difficulties of answered items"""
        return [item.b for item in self.answered_items]

    def get_ability_se(self) -> float:
        """Calculates the current standard error
        of the ability estimation."""
        answered_items_difficulties: List[float] = self.get_answered_items_difficulties()
        return standard_error(answered_items_difficulties, self.ability_level)

    def get_next_item(self) -> TestItem:
        """Selects next item using Urry's rule."""
        item = urrys_rule(self.items, self.ability_level)
        return item

    @abc.abstractmethod
    def estimate_ability_level(self, answered_items_difficulties: List[float]) -> float:
        """
        Estimates ability level.
        Has to be implemented.
        :return: estimated ability level
        """
        pass

    def run_test_once(self):
        """Runs the test once and saves the results
        to self.test_results"""
        # get item
        item = self.get_next_item()
        if self.DEBUG:
            print(f"Selected {item.b} for an ability level of {self.ability_level}.")
        # find response
        response = item.simulated_response
        if self.DEBUG:
            print(f"Response: {response}")

        # add response to response pattern
        self.response_pattern.append(response)
        # add item to answered items list
        self.answered_items.append(item)

        # get item difficulties of answered items
        item_difficulties = self.get_answered_items_difficulties()

        # estimate ability level
        estimation = self.estimate_ability_level(item_difficulties)

        # update estimated ability level
        self.ability_level = estimation
        if self.DEBUG:
            print(f"New estimation is {self.ability_level}")
        # remove item from item pool
        index = self.items.index(item)
        self.items.pop(index)
        if self.DEBUG:
            print(f"Now, there are only {len(self.items)} left in the item pool.")
        # create result
        result: TestResult = TestResult(
            ability_estimation=estimation,
            standard_error=self.get_ability_se(),
            showed_item=item.b,
            response=response,
            test_id=self.simulation_id,
            true_ability_level=self.true_ability_level
        )

        # add result to memory
        self.test_results.append(result)
