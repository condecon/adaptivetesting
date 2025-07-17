import unittest
from adaptivetesting.models import ItemPool
from adaptivetesting.math.estimators import BayesModal, NormalPrior, CustomPrior
import pandas as pd
from scipy.stats import beta
from adaptivetesting.math.estimators import CustomPriorException


class TestBayesModal(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_estimation_4pl(self):
        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1]
        })
        item_pool = ItemPool.load_from_dataframe(items)
        item_pool = ItemPool.load_from_dataframe(items)

        response_pattern = [0, 1, 0]
        response_pattern = [0, 1, 0]
        estimator = BayesModal(
            response_pattern=response_pattern,
            items=item_pool.test_items,
            prior=NormalPrior(0, 1),
            optimization_interval=(-4, 4)
        )

        result = estimator.get_estimation()

        self.assertAlmostEqual(result, -0.4741753, 4)


class TestCustomPrior(unittest.TestCase):
    def test_estimation_4pl(self):
        """Test that the calculation does not fail.
        """
        items = pd.DataFrame({"a": [1.3024, 1.078, 0.8758, 0.5571, 1.225, 0.991, 0.9968, 1.1888, 1.1642, 1.1188],
                              "b": [-0.6265, 0.1836, -0.8356, 1.5953, 0.3295, -0.8205, 0.4874, 0.7383, 0.5758, -0.3054],
                              "c": [0.2052, 0.1618, 0.1957, 0.1383, 0.1324, 0.1973, 0.0058, 0.1193, 0.1831, 0.1732],
                              "d": [0.8694, 0.9653, 0.8595, 0.8112, 0.7677, 0.7749, 0.8291, 0.8797, 0.9155, 0.8517]})
        item_pool = ItemPool.load_from_dataframe(items)

        response_pattern = [0, 0, 1, 1, 1, 0, 0, 0, 0, 1]

        # create custom prior
        prior = CustomPrior(
            beta,
            0.6,
            0.9
        )
        
        estimator = BayesModal(
            response_pattern=response_pattern,
            items=item_pool.test_items,
            prior=prior,
            optimization_interval=(-10, 10)
        )

        result = estimator.get_estimation()
        self.assertAlmostEqual(result, 0.01, places=3)

    def test_wrong_prior_implementation(self):
        items = pd.DataFrame({"a": [1.3024, 1.078, 0.8758, 0.5571, 1.225, 0.991, 0.9968, 1.1888, 1.1642, 1.1188],
                              "b": [-0.6265, 0.1836, -0.8356, 1.5953, 0.3295, -0.8205, 0.4874, 0.7383, 0.5758, -0.3054],
                              "c": [0.2052, 0.1618, 0.1957, 0.1383, 0.1324, 0.1973, 0.0058, 0.1193, 0.1831, 0.1732],
                              "d": [0.8694, 0.9653, 0.8595, 0.8112, 0.7677, 0.7749, 0.8291, 0.8797, 0.9155, 0.8517]})
        item_pool = ItemPool.load_from_dataframe(items)

        response_pattern = [0, 0, 1, 1, 1, 0, 0, 0, 0, 1]

        # create custom prior
        class WrongPrior(NormalPrior):
            pass

        prior = WrongPrior(0, 1)
        
        estimator = BayesModal(
            response_pattern=response_pattern,
            items=item_pool.test_items,
            prior=prior,
            optimization_interval=(-10, 10)
        )

        with self.assertRaises(CustomPriorException):
            estimator.get_estimation()
