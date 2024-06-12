from dataclasses import dataclass
from typing import Dict


@dataclass
class TestResult:
    """Representation of simulation test results"""
    test_id: str
    ability_estimation: float
    standard_error: float
    showed_item: float
    response: int
    true_ability_level: float

    @staticmethod
    def from_dict(dictionary: Dict) -> 'TestResult':
        """Create a TestResult from a dictionary

        Args:
            dictionary: with the fields `test_id`, `ability_estimation`, `standard_error`, `showed_item`, `response`,
            `true_ability_level`
        """
        return TestResult(**dictionary)
