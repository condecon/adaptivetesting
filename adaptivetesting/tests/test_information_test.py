import unittest
from adaptivetesting.math import test_information_function
import numpy as np


class TestInformation(unittest.TestCase):
    def test_information_calculation_tensorflow(self):
        difficulties = np.array([0.7, 0.9, 0.6], dtype="float64")
        ability = np.array([0], dtype="float64")

        result = test_information_function(difficulties, ability)

        self.assertAlmostEqual(result, 0.6559974211, 3)


if __name__ == '__main__':
    unittest.main()
