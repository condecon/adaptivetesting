from typing import List
from .__test_item import TestItem
from ..math.item_selection.__urrys_rule import urrys_rule
from ..math.__standard_error import standard_error
import abc
from .__test_result import TestResult
from .__item_pool import ItemPool


class AdaptiveTest(abc.ABC):
    def __init__(self, item_pool: ItemPool,
                 simulation_id: str,
                 participant_id: int,
                 true_ability_level: float,
                 initial_ability_level: float = 0,
                 simulation: bool = True,
                 DEBUG=False):
        """Abstract implementation of an adaptive test.
        All abstract methods have to be overridden
        to create an instance of this class.

        Abstract methods:
            - estimate_ability_level

        Args:
            item_pool (ItemPool): item pool used for the test

            simulation_id (str): simulation id

            participant_id (int): participant id

            true_ability_level (float): true ability level (must always be set)

            initial_ability_level (float): initially assumed ability level

            simulation (bool): will the test be simulated

            DEBUG (bool): enables debug mode
        """
        self.true_ability_level: float = true_ability_level
        self.simulation_id = simulation_id
        self.participant_id: int = participant_id
        # set start values
        self.ability_level = initial_ability_level
        self.answered_items: List[TestItem] = []
        self.response_pattern: List[int] = []
        self.test_results: List[TestResult] = []
        # load items
        self.item_pool = item_pool

        # debug
        self.DEBUG = DEBUG
        self.simulation = simulation

    def get_item_difficulties(self) -> List[float]:
        """
        Returns:
             List[float]: difficulties of items in the item pool
        """
        return [item.b for item in self.item_pool.test_items]

    def get_answered_items_difficulties(self) -> List[float]:
        """
        Returns:
            List[float]: difficulties of answered items
        """
        return [item.b for item in self.answered_items]
    
    def get_answered_items(self) -> List[TestItem]:
        """
        Returns:
            List[TestItem]: answered items
        """
        return self.answered_items

    def get_ability_se(self) -> float:
        """
        Calculate the current standard error
        of the ability estimation.

        Returns:
            float: standard error of the ability estimation

        """
        answered_items = self.get_answered_items()
        return standard_error(answered_items, self.ability_level)

    def get_next_item(self) -> TestItem:
        """Select next item using Urry's rule.

        Returns:
            TestItem: selected item
        """
        item = urrys_rule(self.item_pool.test_items, self.ability_level)
        return item

    @abc.abstractmethod
    def estimate_ability_level(self) -> float:
        """
        Estimates ability level.
        The method has to be implemented by subclasses.

        Returns:
            float: estimated ability level
        """
        pass

    def get_response(self, item: TestItem) -> int:
        """If the adaptive test is not used for simulation.
        This method is used to get user feedback.

        Args:
            item (TestItem): test item shown to the participant

        Return:
            int: participant's response
        """
        raise NotImplementedError("This functionality is not implemented by default.")

    def run_test_once(self):
        """
        Runs the test procedure once.
        Saves the result to test_results of
        the current instance.
        """
        # get item
        item = self.get_next_item()
        if item is not None:
            if self.DEBUG:
                print(f"Selected {item.b} for an ability level of {self.ability_level}.")

        # check if simulation is running
        response = None
        if self.simulation is True:
            response = self.item_pool.get_item_response(item)
        else:
            # not simulation
            response = self.get_response(item)

        if self.DEBUG:
            print(f"Response: {response}")

        # add response to response pattern
        self.response_pattern.append(response)
        # add item to answered items list
        self.answered_items.append(item)

        # estimate ability level
        estimation = self.estimate_ability_level()

        # update estimated ability level
        self.ability_level = estimation
        if self.DEBUG:
            print(f"New estimation is {self.ability_level}")
        # remove item from item pool
        self.item_pool.delete_item(item)
        if self.DEBUG:
            print(f"Now, there are only {len(self.item_pool.test_items)} left in the item pool.")
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

    def check_se_criterion(self, value: float) -> bool:
        if self.get_ability_se() <= value:
            return True
        else:
            return False

    def check_length_criterion(self, value: float) -> bool:
        if len(self.answered_items) >= value:
            return True
        else:
            return False
