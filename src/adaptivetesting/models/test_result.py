from dataclasses import dataclass


@dataclass
class TestResult:
    """Representation of simulation test results"""
    test_id: str
    ability_estimation: float | str
    standard_error: float | str
    showed_item: float
    response: int
    true_ability_level: float

    @staticmethod
    def from_dict(dictionary: dict) -> 'TestResult':
        """Create a TestResult from a dictionary
        :param dictionary: with the fields 'test_id', 'ability_estimation',
        'standard_error', 'showed_item', 'response',
        'true_ability_level'
        """
        return TestResult(**dictionary)
