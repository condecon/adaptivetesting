from typing import List
import csv
import pathlib
from ..models.__test_result import TestResult
from ..services.__test_results_interface import ITestResults


class CSVContext(ITestResults):
    def __init__(self,
                 simulation_id: str,
                 participant_id: str):
        """Implementation of the ITestResults interface for
        saving test results to the CSV format.
        The resulting CSV file <participant_id>.csv
        will be a standard comma-separated values file.

        Args:
            simulation_id (str): folder name

            participant_id (str): participant id
        """
        super().__init__(simulation_id, participant_id)

    def save(self, test_results: List[TestResult]) -> None:
        """Saves a list of test results to a CSV file
        (<participant_id>.csv).

        Args:
            test_results (List[TestResult]): list of test results
        """
        dir_name = self.simulation_id

        # create directory if it does not already exist
        path = pathlib.Path(f"data/{dir_name}")
        path.mkdir(parents=True, exist_ok=True)

        # Get field names from the first TestResult object
        fieldnames = list(vars(test_results[0]).keys())

        with open(f"data/{dir_name}/{self.participant_id}.csv", "w", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for result in test_results:
                writer.writerow(vars(result))
            
            file.close()

    def load(self) -> List[TestResult]:
        """Loads results from the database.
        The implementation of this method is required
        by the interface. However, it does not have
        any implemented functionality and will throw an error
        if used.

        Returns: List[TestResult]
        """
        raise NotImplementedError("This function is not implemented.")
