from typing import List
from ..models.test_result import TestResult
from ..services.test_results_interface import ITestResults
import pickle


class PickleContext(ITestResults):
    def __init__(self,
                 simulation_id: str,
                 participant_id: int):
        super().__init__(simulation_id, participant_id)

    def save(self, test_results: List[TestResult]) -> None:
        with open(f"{self.filename}_{str(self.participant_id)}.pickle", "wb") as file:
            pickle.dump(test_results, file)
            file.close()

    def load(self) -> List[TestResult]:
        raise NotImplementedError("This  function is not implemented.")
