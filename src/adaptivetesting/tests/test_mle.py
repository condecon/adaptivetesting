import unittest
from ..math.mle_tensorflow import MLE_Tensorflow
from ..math.ml_estimation import MLEstimator
from ..models.algorithm_exception import AlgorithmException
import numpy as np


class TestMLE(unittest.TestCase):

    def test_mle_tensorflow(self):
        response_pattern = np.array([0, 1, 0], dtype="float64")
        difficulties = np.array([0.7, 0.9, 0.6], dtype="float64")
        estimator = MLE_Tensorflow(
            response_pattern=response_pattern,
            item_difficulties=difficulties
        )

        estimation_result = estimator.find_max()

        self.assertAlmostEqual(estimation_result, 0.0375530712, 2)

    def test_ml_estimation(self):
        response_pattern = [0, 1, 0]
        difficulties = [0.7, 0.9, 0.6]
        estimator: MLEstimator = MLEstimator(
            response_pattern,
            difficulties
        )

        result = estimator.get_maximum_likelihood_estimation()

        self.assertAlmostEqual(result, 0.0375530712, 2)

    def test_one_item(self):
        response = np.array([0], dtype="float64")
        dif = np.array([0.9], dtype="float64")

        estimator = MLE_Tensorflow(response, dif)

        with self.assertRaises(AlgorithmException):
            result = estimator.find_max()
            print(f"Estimation Result {result}")

    def test_eid(self):
        response_pattern = [1, 0]
        difficulties = [-1.603, 0.909]
        estimator = MLEstimator(response_pattern, difficulties)

        result = estimator.find_max()

        self.assertAlmostEqual(result, -0.347)

    def test_catr_item_1_2(self):
        response_pattern = [1, 0]
        difficulties = [-2.1851, -0.2897194]
        estimator = MLEstimator(response_pattern, difficulties)

        result = estimator.find_max()

        self.assertAlmostEqual(result, -1.237413, 3)
