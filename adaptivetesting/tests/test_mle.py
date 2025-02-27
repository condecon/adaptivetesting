import unittest
from adaptivetesting.math.estimators import MLEstimator
from adaptivetesting.models import AlgorithmException, ItemPool


class TestMLE(unittest.TestCase):

    def test_ml_estimation(self):
        response_pattern = [0, 1, 0]
        difficulties = [0.7, 0.9, 0.6]

        items = ItemPool.load_from_list(b=difficulties).test_items

        estimator: MLEstimator = MLEstimator(
            response_pattern,
            items
        )

        result = estimator.get_estimation()

        self.assertAlmostEqual(result, 0.0375530712, 2)

    def test_one_item(self):
        response = [0]
        dif = [0.9]
        ability = 0

        items = ItemPool.load_from_list(dif).test_items

        estimator = MLEstimator(response, items)

        with self.assertRaises(AlgorithmException):
            result = estimator.get_estimation()
            print(f"Estimation Result {result}")

    def test_eid(self):
        response_pattern = [1, 0]
        difficulties = [-1.603, 0.909]

        items = ItemPool.load_from_list(difficulties).test_items

        estimator = MLEstimator(response_pattern, items)

        result = estimator.get_estimation()

        self.assertAlmostEqual(round(result, 3), -0.347, places=5)

    def test_catr_item_1_2(self):
        response_pattern = [1, 0]
        difficulties = [-2.1851, -0.2897194]

        items = ItemPool.load_from_list(difficulties).test_items
        estimator = MLEstimator(response_pattern, items)

        result = estimator.get_estimation()

        self.assertAlmostEqual(result, -1.237413, 3)
