from typing import List
import pickle
import pathlib
from ..models.__test_result import TestResult
from ..services.__test_results_interface import ITestResults


class PickleContext(ITestResults):
    def __init__(self,
                 simulation_id: str,
                 participant_id: str):
        """Implementation of the ITestResults interface for
        saving test results to the pickle format.
        The resulting pickle file <simulation_id>.pickle
        will be of the standard pickle format which depends
        on the used python version.

        Args:
            simulation_id (str): folder name

            participant_id (str): participant id
        """
        super().__init__(simulation_id, participant_id)

    def save(self, test_results: List[TestResult]) -> None:
        """Saves a list of test results to a pickle binary file
        (<participant_id>.pickle).

        Args:
            test_results (List[TestResult]): list of test results
        """
        dir_name = self.simulation_id

        # create directory if it does not already exist
        path = pathlib.Path(f"data/{dir_name}")
        path.mkdir(parents=True, exist_ok=True)
        # write results in file
        with open(f"data/{dir_name}/{self.participant_id}.pickle", "wb") as file:
            pickle.dump(test_results, file)
            file.close()

    def load(self) -> List[TestResult]:
        """Loads and returns a list of TestResult objects for a specific participant and simulation.
        The method reads a pickle file located at 'data/{simulation_id}/{participant_id}.pickle'
        and deserializes its contents into a list of TestResult instances.
        Returns:
            List[TestResult]: The list of test results loaded from the pickle file.
        Raises:
            FileNotFoundError: If the specified pickle file does not exist.
            pickle.UnpicklingError: If the file cannot be unpickled.
        """
        foldername = f"data/{self.simulation_id}"

        with open(f"{foldername}/{self.participant_id}.pickle", "rb") as file:
            test_results: list[TestResult] = pickle.load(file)
            file.close()
        return test_results
