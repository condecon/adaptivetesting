from ..models.__adaptive_test import AdaptiveTest
from ..models.__item_pool import ItemPool
from ..models.__test_item import TestItem
from ..services.__estimator_interface import IEstimator
from typing import Protocol
from ..math.item_selection.__maximum_information_criterion import maximum_information_criterion
from ..models.__algorithm_exception import AlgorithmException
from ..implementations.__pre_test import PreTest
from ..models.__test_result import TestResult


class ItemSelectionStrategy(Protocol):
    def select(self, item_pool: ItemPool, ability: float, **kwargs) -> TestItem:
        ...


class TestAssembler(AdaptiveTest):
    def __init__(self,
                 item_pool,
                 simulation_id,
                 participant_id,
                 ability_estimator: IEstimator,
                 estimator_args: dict[str, any] = {
                     "prior": None,
                     "optimization_interval": (-10, 10)
                 },
                 item_selector: ItemSelectionStrategy = maximum_information_criterion,
                 item_selector_args: dict[str, any] = {},
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
        estimator: IEstimator = self.__ability_estimator(
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
        item = self.__item_selector(
            self.item_pool.test_items,
            self.ability_level,
            **self.__item_selector_args
        )
        return item

    def run_test_once(self):
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

                if self.debug:
                    print(f"Response: {response}")
                # add response to response pattern
                self.response_pattern.append(response)
                # add item to answered items list
                self.answered_items.append(item)

                # remove items
                self.item_pool.delete_item(item)
            # estimate ability level
            estimation, sd_error = self.estimate_ability_level()
            # create test results for all n-1 random items
            for i in range(0, len(random_items) - 1):
                result = TestResult(
                    ability_estimation=float("nan"),
                    standard_error=float("nan"),
                    showed_item=random_items[i].b,
                    response=self.response_pattern[i],
                    test_id=self.simulation_id,
                    true_ability_level=self.true_ability_level,
                )
                # append to memory
                self.test_results.append(result)

            # create test result for first ability estimation
            intermediate_result = TestResult(
                ability_estimation=self.ability_level,
                standard_error=self.standard_error,
                showed_item=random_items[-1].b,
                response=self.response_pattern[-1],
                test_id=self.simulation_id,
                true_ability_level=self.true_ability_level,
            )
            self.test_results.append(intermediate_result)

        return super().run_test_once()
