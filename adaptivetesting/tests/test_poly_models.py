# flake8: noqa
import adaptivetesting as adt
import unittest

class TestPolyMLEstimation(unittest.TestCase):
    def test_grm(self):
        items = adt.ItemPool.load_from_list(
            a = [0.943, 0.972, 1.210],
            b = [
                [0.071, 0.129],
                [0.461, 1.715],
                [-1.265, -0.687]
            ]
        ).test_items

        pattern = [2, 1, 2]
        estimator = adt.MLEstimator(
            response_pattern=pattern,
            items=items,
            model="GRM"
        )
        estimate = estimator.get_estimation()
        print(estimate)
        self.assertAlmostEqual(1.6684, round(estimate, 3), delta=0.001)

        pattern = [0, 1, 2]
        estimator = adt.MLEstimator(
            response_pattern=pattern,
            items=items,
            model="GRM"
        )
        estimate = estimator.get_estimation()
        self.assertAlmostEqual(0.4076371, estimate, delta=0.01)

    def test_gpcm(self):
        items = adt.ItemPool.load_from_list(
            a = [0.934, 0.972, 1.210],
            b = [
                [0.071, 0.129],
                [1.715, 0.461],
                [-1.265, -0.687]
            ]
        ).test_items

        pattern = [2,1,2]
        estimator = adt.MLEstimator(
            pattern,
            items,
            "GPCM"
        )
        estimate = estimator.get_estimation()
        self.assertAlmostEqual(
            1.581,
            estimate,
            delta=0.001
        )

        pattern = [0, 1, 2]
        estimator = adt.MLEstimator(
            pattern,
            items,
            "GPCM"
        )
        estimate = estimator.get_estimation()
        self.assertAlmostEqual(
            0.181,
            estimate,
            delta=0.001
        )

    def test_gpcm_information(self):
        items = adt.ItemPool.load_from_list(
            a = [0.934, 0.972, 1.210],
            b = [
                [0.071, 0.129],
                [1.715, 0.461],
                [-1.265, -0.687]
            ]
        ).test_items

        pattern = [2, 1, 2] # required for spec, has no influence on the result
        estimator = adt.MLEstimator(pattern,
                                    items,
                                    "GPCM")
        sde = estimator.get_standard_error(0)
        self.assertAlmostEqual(sde, 0.819, delta=0.001)

    def test_grm_information(self):
        items = adt.ItemPool.load_from_list(
            a = [0.943, 0.972, 1.210],
            b = [
                [0.071, 0.129],
                [0.461, 1.715],
                [-1.265, -0.687]
            ]
        ).test_items

        pattern = [2, 1, 2] # required for spec, has no influence on the result
        estimator = adt.MLEstimator(pattern,
                                    items,
                                    "GRM")
        sde = estimator.get_standard_error(0)
        self.assertAlmostEqual(sde, 1.133, delta=0.003)
