from abc import ABC, abstractmethod
from ..models.test_result import TestResult
from typing import List


class ITestResults(ABC):
    """Interface for saving test results to database"""
    def __init__(self, simulation_id: str, participant_id: int):
        self.filename = f"data/{simulation_id}.db"
        self.participant_id: int = participant_id

    @abstractmethod
    def save(self, test_results: List[TestResult]) -> None:
        pass

    @abstractmethod
    def load(self) -> List[TestResult]:
        pass
