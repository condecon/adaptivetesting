from ..models.__adaptive_test import AdaptiveTest
from ..models.__item_pool import ItemPool
from ..models.__algorithm_exception import AlgorithmException
from ..models.__test_result import TestResult
from ..math.estimators.__ml_estimation import MLEstimator
from .__pre_test import PreTest


class SemiAdaptiveImplementation(AdaptiveTest):

    def __init__(self,
                 item_pool: ItemPool,
                 simulation_id: str,
                 participant_id: int,
                 true_ability_level: float,
                 initial_ability_level: float = 0,
                 simulation=True,
                 debug=False,
                 pretest_seed=12345):
        """
        This class represents the Semi-Adaptive implementation using
        Maximum Likelihood Estimation and Urry's rule during the test.
        The pretest is 4 items long.

        Args:
            item_pool (ItemPool): item pool used for the test

            simulation_id (str): simulation id

            participant_id (int): participant id

            true_ability_level (float): true ability level (must always be set)

            initial_ability_level (float): initially assumed ability level

            simulation (bool): will the test be simulated

            debug (bool): enables debug mode

            pretest_seed (int): seed used for the random number generator to draw pretest items.

        """

        super().__init__(item_pool,
                         simulation_id,
                         participant_id,
                         true_ability_level,
                         initial_ability_level,
                         simulation,
                         debug)

        self.pretest_seed = pretest_seed

    def estimate_ability_level(self) -> float:
        """
        Estimates latent ability level using ML.
        If responses are only 1 or 0,
        the ability will be set to one
        of the boundaries of the estimation interval (`[-10,10]`).

        Returns:
            float: ability estimation
        """
        estimator = MLEstimator(
            self.response_pattern,
            self.get_answered_items()
        )
        estimation: float = float("NaN")
        try:
            estimation = estimator.get_estimation()
        except AlgorithmException as exception:
            # check if all responses are the same
            if len(set(self.response_pattern)) == 1:
                if self.response_pattern[0] == 0:
                    estimation = -10
                elif self.response_pattern[0] == 1:
                    estimation = 10

            else:
                raise AlgorithmException("""Something else
                    when wrong when running MLE""") from exception

        return estimation

    def pre_test(self):
        """Runs pretest"""
        # create test instance
        pretest = PreTest(
            items=self.item_pool.test_items,
            seed=self.pretest_seed
        )
        # get selected items
        random_items = pretest.select_random_item_quantile()

        # get responses
        for item in random_items:
            response = self.item_pool.get_item_response(item)
            # add response to response pattern
            self.response_pattern.append(response)
            # add item to answered items list
            self.answered_items.append(item)

        # remove random items from item pool
        for item in random_items:
            self.item_pool.delete_item(item)

        # estimate ability level
        estimation = self.estimate_ability_level()
        self.ability_level = estimation

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
            standard_error=self.get_ability_se(),
            showed_item=random_items[-1].b,
            response=self.response_pattern[-1],
            test_id=self.simulation_id,
            true_ability_level=self.true_ability_level,
        )
        self.test_results.append(intermediate_result)
