from ..models.__adaptive_test import AdaptiveTest
from typing import Type, Any
from ..services.__estimator_interface import IEstimator
from .__test_assembler import EstimatorArgs


class PolyTestAssembler(AdaptiveTest):
    def __init__(self,
                 item_pool,
                 simulation_id,
                 participant_id,
                 ability_estimator: Type[IEstimator],
                 estimator_args: EstimatorArgs = {
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
                 DEBUG=False,
                 **kwargs):
        super().__init__(item_pool, simulation_id, participant_id,
                         true_ability_level, initial_ability_level, simulation, DEBUG, **kwargs)

        self.__ability_estimator = ability_estimator
        self.__estimator_args = estimator_args
        self.__item_selector = item_selector
        self.__item_selector_args = item_selector_args
        self.__pretest = pretest
        self.__pretest_seed = pretest_seed