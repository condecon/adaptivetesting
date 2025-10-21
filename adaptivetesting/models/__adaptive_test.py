from typing import List
import abc
import copy
from .__test_item import TestItem
from ..math.item_selection.__urrys_rule import urrys_rule
from ..math.__gen_response_pattern import generate_response_pattern
from .__test_result import TestResult
from .__item_pool import ItemPool


class AdaptiveTest(abc.ABC):
    def __init__(self, item_pool: ItemPool,
                 simulation_id: str,
                 participant_id: str,
                 true_ability_level: float | None = None,
                 initial_ability_level: float = 0,
                 simulation: bool = True,
                 DEBUG=False,
                 **kwargs):
        """Abstract implementation of an adaptive test.
        All abstract methods have to be overridden
        to create an instance of this class.

        Abstract methods:
            - estimate_ability_level

        Args:
            item_pool (ItemPool): item pool used for the test

            simulation_id (str): simulation id

            participant_id (str): participant id

            true_ability_level (float): true ability level (must always be set)

            initial_ability_level (float): initially assumed ability level

            simulation (bool): will the test be simulated.
                If it is simulated and a response pattern is not yet set in the item pool,
                it will be generated for the given true ability level.
                A seed may also be set using the additional argument `seed` and set it to an int value, e.g.
                `AdaptiveTest(..., seed=1234)`

            DEBUG (bool): enables debug mode
        """
        self.true_ability_level = true_ability_level
        self.simulation_id = simulation_id
        self.participant_id = participant_id
        # set start values
        self.ability_level = initial_ability_level
        self.standard_error = float("NaN")
        self.answered_items: List[TestItem] = []
        self.response_pattern: List[int] = []
        self.test_results: List[TestResult] = []
        # make a deep copy of the item pool so
        # that it can be referenced by other instances as well
        # without modifying all other instances
        self.item_pool = copy.deepcopy(item_pool)

        # debug
        self.DEBUG = DEBUG
        self.simulation = simulation

        # if simulation is True
        # generate a response pattern if
        # it is not yet set in the item pool
        if simulation is True:
            if self.item_pool.simulated_responses is None:
                if self.true_ability_level is not None:
                    self.item_pool.simulated_responses = generate_response_pattern(
                        ability=self.true_ability_level,
                        items=self.item_pool.test_items,
                        seed=kwargs["seed"] if "seed" in kwargs.keys() else None
                    )

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

    # def get_ability_se(self) -> float:
    #     """
    #     Calculate the current standard error
    #     of the ability estimation.

    #     Returns:
    #         float: standard error of the ability estimation

    #     """
    #     answered_items = self.get_answered_items()
    #     return standard_error(answered_items, self.ability_level)

    @abc.abstractmethod
    def get_next_item(self) -> TestItem:
        """Select next item.

        Returns:
            TestItem: selected item
        """
        raise NotImplementedError("This functionality is not implemented by default.")
        item = urrys_rule(self.item_pool.test_items, self.ability_level)
        return item

    @abc.abstractmethod
    def estimate_ability_level(self) -> tuple[float, float]:
        """
        Estimates ability level.
        The method has to be implemented by subclasses.

        Returns:
            (float, float): estimated ability level, standard error of the estimation
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
        estimation, sd_error = self.estimate_ability_level()

        # update estimated ability level and standard error
        self.ability_level = estimation
        self.standard_error = sd_error
        if self.DEBUG:
            print(f"New estimation is {self.ability_level} with standard error {self.standard_error}.")

        # remove item from item pool
        self.item_pool.delete_item(item)
        if self.DEBUG:
            print(f"Now, there are only {len(self.item_pool.test_items)} left in the item pool.")
        # create result
        result: TestResult = TestResult(
            ability_estimation=float(estimation),
            standard_error=self.standard_error,
            showed_item=item.as_dict(),
            response=response,
            test_id=self.simulation_id,
            true_ability_level=self.true_ability_level if self.true_ability_level is not None else float("NaN")
        )

        # add result to memory
        self.test_results.append(result)

    def check_se_criterion(self, value: float) -> bool:
        if self.standard_error <= value:
            return True
        else:
            return False

    def check_length_criterion(self, value: float) -> bool:
        if len(self.answered_items) >= value:
            return True
        else:
            return False
