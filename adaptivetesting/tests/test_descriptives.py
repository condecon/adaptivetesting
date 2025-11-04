import unittest
from unittest.mock import patch
import numpy as np
from adaptivetesting import rmse, bias, average_absolute_deviation, TestResult
from adaptivetesting.models.__misc import ResultOutputFormat


class DummyResult:
    def __init__(self, ability_estimation, true_ability_level):
        self.ability_estimation = ability_estimation
        self.true_ability_level = true_ability_level


class TestDescriptives(unittest.TestCase):
    @patch('adaptivetesting.utils.__descriptives.load_final_test_results')
    def test_bias(self, mock_load):
        mock_load.return_value = [
            TestResult(None, 1.0, None, None, None, 0.5), # type: ignore
            TestResult(None, 2.0, None, None, None, 1.5), # type: ignore
            TestResult(None, 3.0, None, None, None, 2.5), # type: ignore
        ]
        result = bias('sim1', ['p1', 'p2', 'p3'], ResultOutputFormat.CSV)
        expected = np.mean([1.0 - 0.5, 2.0 - 1.5, 3.0 - 2.5])
        self.assertAlmostEqual(result, expected) # type: ignore

    @patch('adaptivetesting.utils.__descriptives.load_final_test_results')
    def test_average_absolute_deviation(self, mock_load):
        mock_load.return_value = [
            TestResult(None, 1.0, None, None, None, 0.5), # type: ignore
            TestResult(None, 2.0, None, None, None, 1.5), # type: ignore
            TestResult(None, 3.0, None, None, None, 2.5), # type: ignore
        ]
        result = average_absolute_deviation('sim1', ['p1', 'p2', 'p3'], ResultOutputFormat.CSV)
        expected = np.mean([abs(1.0 - 0.5), abs(2.0 - 1.5), abs(3.0 - 2.5)])
        self.assertAlmostEqual(result, expected) # type: ignore

    @patch('adaptivetesting.utils.__descriptives.load_final_test_results')
    def test_rmse(self, mock_load):
        mock_load.return_value = [
            TestResult(None, 1.0, None, None, None, 0.5), # type: ignore
            TestResult(None, 2.0, None, None, None, 1.5), # type: ignore
            TestResult(None, 3.0, None, None, None, 2.5), # type: ignore
        ]
        result = rmse('sim1', ['p1', 'p2', 'p3'], ResultOutputFormat.CSV)
        expected = np.sqrt(np.mean([(1.0 - 0.5) ** 2, (2.0 - 1.5) ** 2, (3.0 - 2.5) ** 2]))
        self.assertAlmostEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
