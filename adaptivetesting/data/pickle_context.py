from typing import List
import pickle
import pathlib
from adaptivetesting.models import TestResult
from adaptivetesting.services import ITestResults


class PickleContext(ITestResults):
    def __init__(self,
                 simulation_id: str,
                 participant_id: int):
        super().__init__(simulation_id, participant_id)

    def save(self, test_results: List[TestResult]) -> None:
        dir_name = self.simulation_id

        # create directory if it does not already exist
        path = pathlib.Path(f"data/{dir_name}")
        path.mkdir(parents=True, exist_ok=True)
        # write results in file
        with open(f"data/{dir_name}/{str(self.participant_id)}.pickle", "wb") as file:
            pickle.dump(test_results, file)
            file.close()

    def load(self) -> List[TestResult]:
        raise NotImplementedError("This  function is not implemented.")
