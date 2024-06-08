from ..models.adaptive_test import AdaptiveTest
from ..data.sqlite_context import SQLiteContext
from ..data.pickle_context import PickleContext
from ..services.test_results_interface import ITestResults
from enum import Enum


class ResultOutputFormat(Enum):
    SQLITE = 1
    PICKLE = 2


class StoppingCriterion(Enum):
    SE = 1
    LENGTH = 2


class Simulation:
    def __init__(self,
                 test: AdaptiveTest,
                 test_result_output: ResultOutputFormat):
        self.test = test
        self.test_result_output = test_result_output

    def simulate(self,
                 criterion: StoppingCriterion = StoppingCriterion.SE,
                 value: float = 0.4):
        """Runs test until the criterion is met."""
        stop_test = False
        while stop_test is False:
            # run test
            self.test.run_test_once()
            # check available items
            if len(self.test.item_pool.test_items) == 0:
                stop_test = True
            else:
                if criterion == StoppingCriterion.SE:
                    stop_test = self.test.check_se_criterion(value)
                elif criterion == StoppingCriterion.LENGTH:
                    stop_test = self.test.check_length_criterion(value)

    def save_test_results(self):
        """Saves test results to the specified output format."""
        data_context: ITestResults
        if self.test_result_output == ResultOutputFormat.PICKLE:
            data_context = PickleContext(simulation_id=self.test.simulation_id,
                                         participant_id=self.test.participant_id)
        else:
            data_context = SQLiteContext(
                simulation_id=self.test.simulation_id,
                participant_id=self.test.participant_id
            )
        # save results
        data_context.save(self.test.test_results)
