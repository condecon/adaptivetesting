from typing import List
import pickle
import pathlib
from ..models.__test_result import TestResult
from ..services.__test_results_interface import ITestResults


class PickleContext(ITestResults):
    def __init__(self,
                 simulation_id: str,
                 participant_id: int):
        """Implementation of the ITestResults interface for
        saving test results to the pickle format.
        The resulting pickle file <simulation_id>.pickle
        will be of the standard pickle format which depends
        on the used python version.

        Args:
            simulation_id (str): Not used but required by the interface

            participant_id (int): participant id and table name
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
        with open(f"data/{dir_name}/{str(self.participant_id)}.pickle", "wb") as file:
            pickle.dump(test_results, file)
            file.close()

    def load(self) -> List[TestResult]:
        """Loads results from the database.
        The implementation of this method is required
        by the interface. However, is does not have
        any implemented functionality and will throw an error
        if used.

        Returns: List[TestResult]
        """
        raise NotImplementedError("This  function is not implemented.")
