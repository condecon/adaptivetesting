from ..models.__adaptive_test import AdaptiveTest
from ..models.__test_item import TestItem
from ..services.__estimator_interface import IEstimator
from typing import Any, Type
from ..math.item_selection.__maximum_information_criterion import maximum_information_criterion
from ..models.__algorithm_exception import AlgorithmException
from ..implementations.__pre_test import PreTest
from ..models.__test_result import TestResult
from ..services.__item_selection_protocol import ItemSelectionStrategy


class TestAssembler(AdaptiveTest):
    """
    TestAssembler is a subclass of AdaptiveTest designed to assemble and administer adaptive tests,
    optionally including a pretest phase. It supports customizable ability estimation and item selection strategies.
    Args:
        
        item_pool: The pool of test items available for selection.
        
        simulation_id: Identifier for the simulation run.
        
        participant_id: Identifier for the participant.
        
        ability_estimator (Type[IEstimator]): The estimator class used for ability estimation.
        
        estimator_args (dict[str, Any], optional):
            Arguments for the ability estimator. Defaults to {"prior": None, "optimization_interval": (-10, 10)}.
        
        item_selector (ItemSelectionStrategy, optional):
            Function or strategy for selecting the next item. Defaults to maximum_information_criterion.
        
        item_selector_args (dict[str, Any], optional): Arguments for the item selector. Defaults to {}.
        
        pretest (bool, optional): Whether to run a pretest phase before the main test. Defaults to False.
        
        pretest_seed (int | None, optional): Random seed for pretest item selection. Defaults to None.
        
        true_ability_level (optional): The true ability level of the participant (for simulation).
        
        initial_ability_level (optional): The initial ability estimate. Defaults to 0.
        
        simulation (bool, optional): Whether the test is run in simulation mode. Defaults to True.
        
        debug (bool, optional): Whether to enable debug output. Defaults to False.
        
        **kwargs: Additional keyword arguments passed to the AdaptiveTest superclass.
    
    Methods:
        estimate_ability_level():
            Estimates the current ability level using the specified estimator and handles exceptions
            for specific response patterns (all correct or all incorrect).
        
        get_next_item() -> TestItem:
            Selects the next item to administer using the specified item selection strategy.
        
        run_test_once():
            Runs a single iteration of the test, including an optional pretest phase. Handles item
            administration, response collection, ability estimation, and result recording.
    
    Attributes:
        __ability_estimator: The estimator class for ability estimation.
        
        __estimator_args: Arguments for the ability estimator.
        
        __item_selector: The item selection strategy.
        
        __item_selector_args: Arguments for the item selector.
        
        __pretest: Whether to run a pretest phase.
        
        __pretest_seed: Random seed for pretest item selection.
    """
    def __init__(self,
                 item_pool,
                 simulation_id,
                 participant_id,
                 ability_estimator: Type[IEstimator],
                 estimator_args: dict[str, Any] = {
                     "prior": None,
                     "optimization_interval": (-10, 10)
                 },
                 item_selector: ItemSelectionStrategy = maximum_information_criterion, # type: ignore
                 item_selector_args: dict[str, Any] = {},
                 pretest: bool = False,
                 pretest_seed: int | None = None,
                 true_ability_level=None,
                 initial_ability_level=0,
                 simulation=True,
                 debug=False,
                 **kwargs):
        self.__ability_estimator = ability_estimator
        self.__estimator_args = estimator_args
        self.__item_selector = item_selector
        self.__item_selector_args = item_selector_args
        self.__pretest = pretest
        self.__pretest_seed = pretest_seed
            
        super().__init__(item_pool,
                         simulation_id,
                         participant_id,
                         true_ability_level,
                         initial_ability_level,
                         simulation,
                         debug,
                         **kwargs)
    
    def estimate_ability_level(self):
        """
        Estimates the ability level of a test-taker based on their response pattern and answered items.
        This method uses the configured ability estimator to calculate the ability estimation and its standard error.
        If an AlgorithmException occurs during estimation,
        and all responses are identical (all correct or all incorrect),
        it assigns a default estimation value (-10 for all incorrect, 10 for all correct)
        and recalculates the standard error.
        Otherwise, it raises an AlgorithmException with additional context.
        
        Returns:
            tuple[float, float]: A tuple containing the estimated ability level (float) and its standard error (float).
        
        Raises:
            AlgorithmException: If estimation fails for reasons other than all responses being identical.
        """
        estimator = self.__ability_estimator(
            self.response_pattern,
            self.answered_items,
            **self.__estimator_args
        )

        try:
            estimation = estimator.get_estimation()
            standard_error = estimator.get_standard_error(estimation)
        except AlgorithmException as exception:
            # check if all responses are the same
            if len(set(self.response_pattern)) == 1:
                if self.response_pattern[0] == 0:
                    estimation = -10
                elif self.response_pattern[0] == 1:
                    estimation = 10
                standard_error = estimator.get_standard_error(estimation)

            else:
                raise AlgorithmException(f"""Something
                when wrong when running {type(estimator)}""") from exception

        return estimation, standard_error
    
    def get_next_item(self) -> TestItem:
        """
        Selects and returns the next test item based on the current ability level and item selector strategy.

        Returns:
            TestItem: The next item to be administered in the test, as determined by the item selector.

        Raises:
            Any exceptions raised by the item selector function.
        """
        item = self.__item_selector(
            self.item_pool.test_items,
            self.ability_level,
            **self.__item_selector_args
        )
        return item

    def run_test_once(self):
        """
        Executes a single run of the test, including optional pretest logic.
        If pretesting is enabled, this method:
            - Selects a random quantile of items from the item pool using a PreTest instance.
            - For each selected item:
                - Obtains a response (either simulated or real).
                - Appends the response and item to the respective lists.
                - Removes the item from the item pool.
            - Estimates the ability level and standard error after pretest responses.
            - Records test results for each pretest item, with the final item including the first ability estimation.
        
        Returns:
            The result of the superclass's run_test_once() method.
        """
        # check if to run pretest
        if self.__pretest is True:
            pretest = PreTest(
                self.item_pool.test_items,
                self.__pretest_seed
            )
            # get selected items
            random_items = pretest.select_random_item_quantile()
            for item in random_items:
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

                # remove items
                self.item_pool.delete_item(item)
            # estimate ability level
            estimation, sd_error = self.estimate_ability_level()
            self.ability_level = estimation
            self.standard_error = sd_error
            # create test results for all n-1 random items
            for i in range(0, len(random_items) - 1):
                result = TestResult(
                    ability_estimation=float("nan"),
                    standard_error=float("nan"),
                    showed_item=random_items[i].as_dict(),
                    response=self.response_pattern[i],
                    test_id=self.simulation_id,
                    true_ability_level=self.true_ability_level if self.true_ability_level is not None else float("NaN"),
                )
                # append to memory
                self.test_results.append(result)

            # create test result for first ability estimation
            intermediate_result = TestResult(
                ability_estimation=self.ability_level,
                standard_error=self.standard_error,
                showed_item=random_items[-1].as_dict(),
                response=self.response_pattern[-1],
                test_id=self.simulation_id,
                true_ability_level=self.true_ability_level if self.true_ability_level is not None else float("NaN"),
            )
            self.test_results.append(intermediate_result)

        return super().run_test_once()
