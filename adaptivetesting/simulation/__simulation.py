from ..models.__adaptive_test import AdaptiveTest
from ..models.__test_result import TestResult
from ..data.__sqlite_context import SQLiteContext
from ..data.__pickle_context import PickleContext
from ..services.__test_results_interface import ITestResults
from enum import Enum
from multiprocessing import Pool


class ResultOutputFormat(Enum):
    """
    Enum for selecting the output format for
    the test results
    """
    SQLITE = 1
    PICKLE = 2


class StoppingCriterion(Enum):
    """Enum for selecting the stopping criterion
    for the adaptive test"""
    SE = 1
    LENGTH = 2


class Simulation:
    def __init__(self,
                 test: AdaptiveTest,
                 test_result_output: ResultOutputFormat):
        """
        This class can be used for simulating CAT.

        Args:
            test (AdaptiveTest): instance of an adaptive test implementation (see implementations module)

            test_result_output (ResultOutputFormat): test results output format
        """
        self.test = test
        self.test_result_output = test_result_output

    def simulate(self,
                 criterion: StoppingCriterion = StoppingCriterion.SE,
                 value: float = 0.4):
        """Runs test until the stopping criterion is met.

        Args:
            criterion (StoppingCriterion): selected stopping criterion

            value (float): either standard error value or test length value that has to be met by the test

        """
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
        """Saves the test results to the specified output format."""
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


def setup_simulation_and_start(test: AdaptiveTest,
                               test_result_output: ResultOutputFormat,
                               criterion: StoppingCriterion,
                               value: float):
    """
    Args:
        test (AdaptiveTest): _description_
    """
    simulation = Simulation(test=test,
                            test_result_output=test_result_output)
    simulation.simulate(criterion=criterion,
                        value=value)
    # save results
    simulation.save_test_results()

class SimulationPool():
    def __init__(self,
                 adaptive_tests: list[AdaptiveTest],
                 test_result_output: ResultOutputFormat,
                 criterion: StoppingCriterion = StoppingCriterion.SE,
                 value: float = 0.4):
        self.adaptive_tests = adaptive_tests
        self.test_results_output = test_result_output
        self.criterion = criterion
        self.value = value
        
    def start(self):
        with Pool(len(self.adaptive_tests)) as pool:
            pool.map(lambda test: setup_simulation_and_start(test,
                                                             self.test_results_output,
                                                             self.criterion,
                                                             self.value),
                                                             self.adaptive_tests)
