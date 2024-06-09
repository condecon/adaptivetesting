from typing import List
from ..models.adaptive_test import AdaptiveTest
from ..models.item_pool import ItemPool
from ..models.algorithm_exception import AlgorithmException
from ..math import MLEstimator


class DefaultImplementation(AdaptiveTest):

    def __init__(self, item_pool: ItemPool,
                 simulation_id: str,
                 participant_id: int,
                 true_ability_level: float,
                 initial_ability_level: float = 0,
                 simulation=True,
                 debug=False):
        """

        :param items:
        :param simulation_id:
        :param participant_id:
        :param true_ability_level:
        :param initial_ability_level:
        :param DEBUG:
        """
        super().__init__(item_pool,
                         simulation_id,
                         participant_id,
                         true_ability_level,
                         initial_ability_level,
                         simulation,
                         debug)

    def estimate_ability_level(self, answered_items_difficulties: List[float]) -> float:
        """
        Estimates latent ability level using ML.
        If responses are only 1 or 0, extreme values
        of the distribution are returned.
        
        Args:
            answered_items_difficulties (List[float]): List of difficulty valus of the answered items

        
        Returns:
            estimation: ability estimation
        """
        estimator = MLEstimator(
            self.response_pattern,
            self.get_answered_items_difficulties()
        )
        estimation: float = float("NaN")
        try:
            estimation = estimator.get_maximum_likelihood_estimation()
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
