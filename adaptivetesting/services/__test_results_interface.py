from abc import ABC, abstractmethod
from ..models.__test_result import TestResult
from typing import List


class ITestResults(ABC):

    def __init__(self, simulation_id: str, participant_id: int):
        """Interface for saving and reading test results.
        This interface may mainly be used for saving simulation results.

        Args:
            simulation_id (str): The simulation ID. Name of the results file.

            participant_id (int): The participant ID.
        """
        self.simulation_id = simulation_id
        self.filename = f"data/{self.simulation_id}.db"
        self.participant_id: int = participant_id

    @abstractmethod
    def save(self, test_results: List[TestResult]) -> None:
        pass

    @abstractmethod
    def load(self) -> List[TestResult]:
        pass
