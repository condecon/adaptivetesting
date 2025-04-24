from ..models.__adaptive_test import AdaptiveTest
from ..models.__item_pool import ItemPool
from ..models.__algorithm_exception import AlgorithmException
from ..math.estimators.__ml_estimation import MLEstimator


class DefaultImplementation(AdaptiveTest):
    """This class represents the Default implementation using
    Maximum Likelihood Estimation and Urry's rule during the test."""
    def __init__(self, item_pool: ItemPool,
                 simulation_id: str,
                 participant_id: int,
                 true_ability_level: float,
                 initial_ability_level: float = 0,
                 simulation=True,
                 debug=False):
        """
        Args:
            item_pool (ItemPool): item pool used for the test

            simulation_id (str): simulation id

            participant_id (int): participant id

            true_ability_level (float): true ability level (must always be set)

            initial_ability_level (float): initially assumed ability level

            simulation (bool): will the test be simulated

            debug (bool): enables debug mode

        """
        super().__init__(item_pool,
                         simulation_id,
                         participant_id,
                         true_ability_level,
                         initial_ability_level,
                         simulation,
                         debug)

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
