from ..models.__adaptive_test import AdaptiveTest
from ..data.__csv_context import CSVContext
from ..data.__pickle_context import PickleContext
from ..services.__test_results_interface import ITestResults
from ..models.__misc import ResultOutputFormat, StoppingCriterion
from functools import partial
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from tqdm import tqdm
import platform


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
                 criterion: StoppingCriterion | list[StoppingCriterion] = StoppingCriterion.SE,
                 value: float | list[float | int] = 0.4):
        """
        Runs the adaptive test simulation until the specified stopping criterion or criteria are met.

        Args:
            criterion (StoppingCriterion | list[StoppingCriterion]):
                The stopping criterion or list of criteria to determine when the test should stop.
                Supported values are StoppingCriterion.SE (standard error) and StoppingCriterion.LENGTH (test length).

            value (float | list[float | int]):
                The threshold value(s) for the stopping criterion. For SE, this is the maximum allowed standard error.
                For LENGTH, this is the maximum number of items administered.

        """
        stop_test = False
        while stop_test is False:
            # run test
            self.test.run_test_once()
            # check available items
            if len(self.test.item_pool.test_items) == 0:
                stop_test = True
            else:
                # Support both single criterion and list of criteria/values
                criteria = criterion if isinstance(criterion, list) else [criterion]
                values = value if isinstance(value, list) else [value]
                stop_test = any(
                    self.test.check_se_criterion(v) if c == StoppingCriterion.SE
                    else self.test.check_length_criterion(v) if c == StoppingCriterion.LENGTH
                    else False
                    for c, v in zip(criteria, values)
                )

    def save_test_results(self):
        """Saves the test results to the specified output format."""
        data_context: ITestResults
        if self.test_result_output == ResultOutputFormat.PICKLE:
            data_context = PickleContext(simulation_id=self.test.simulation_id,
                                         participant_id=self.test.participant_id)
        else:
            data_context = CSVContext(
                simulation_id=self.test.simulation_id,
                participant_id=self.test.participant_id
            )
        # save results
        data_context.save(self.test.test_results)


def setup_simulation_and_start(test: AdaptiveTest,
                               test_result_output: ResultOutputFormat,
                               criterion: StoppingCriterion | list[StoppingCriterion],
                               value: float):
    """
    Sets up and runs a simulation for an adaptive test, then saves the results.

    Args:
        test (AdaptiveTest): The adaptive test instance to be simulated.
        
        test_result_output (ResultOutputFormat): The format or handler for outputting test results.
        
        criterion (StoppingCriterion | list[StoppingCriterion]):
            The criterion used to determine when the simulation should stop.
        
        value (float):
            The value associated with the stopping criterion (e.g., maximum number of items, target standard error).
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
                 criterion: StoppingCriterion | list[StoppingCriterion] = StoppingCriterion.SE,
                 value: float = 0.4):
        """
        A pool manager for running multiple adaptive test simulations in parallel.
        
        Args:
            adaptive_tests (list[AdaptiveTest]): List of adaptive test instances to be simulated.
            
            test_results_output (ResultOutputFormat): Format for outputting test results.
            
            criterion (StoppingCriterion | list[StoppingCriterion]):
                Stopping criterion or list of criteria for the simulations.
            
            value (float): Value associated with the stopping criterion (default is 0.4).
        """
        self.adaptive_tests = adaptive_tests
        self.test_results_output = test_result_output
        self.criterion = criterion
        self.value = value
        
    def start(self):
        """
        Starts the simulation by executing adaptive tests in parallel.

        Depending on the operating system, uses either multithreading (on Windows)
        or multiprocessing (on other platforms) to run the simulation for each adaptive test.
        Progress is displayed using a progress bar.
        """
        func = partial(
            setup_simulation_and_start,
            test_result_output=self.test_results_output,
            criterion=self.criterion,
            value=self.value
        )
        # check for platform
        # this is because multiprocessing is not as well supported on windows
        # therefore, multithreading is used instead
        if platform.system() == "Windows":
            with ThreadPoolExecutor(max_workers=60) as executor:
                futures = [executor.submit(func, test) for test in self.adaptive_tests]
                for _ in tqdm(as_completed(futures), total=len(futures)):
                    pass
        else:
            with ProcessPoolExecutor() as executor:
                futures = [executor.submit(func, test) for test in self.adaptive_tests]
                for _ in tqdm(as_completed(futures), total=len(futures)):
                    pass
