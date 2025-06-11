import unittest
from typing import List
from adaptivetesting.models import ItemPool, TestItem
from adaptivetesting.math.estimators import MLEstimator, ExpectedAPosteriori, BayesModal, NormalPrior, CustomPrior
import pandas as pd
from scipy.stats import beta, f
import math


class TestStandardError(unittest.TestCase):
    def test_dummy_items(self):
        items = [0.7, 0.9, 0.6]
        ability = 0

        item_list: List[TestItem] = ItemPool.load_from_list(items).test_items
        estimator = MLEstimator([], item_list)
        result = estimator.get_standard_error(ability)

        self.assertAlmostEqual(result, 1.234664423, 3)

    def test_eid_items(self):
        items = [-1.603, 0.909]
        ability = -0.347

        item_list = ItemPool.load_from_list(items).test_items
        estimator = MLEstimator([], item_list)
        result = estimator.get_standard_error(ability)

        self.assertAlmostEqual(result, 1.702372, 3)

    def test_calculation_4pl(self):
        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1]
        })

        item_pool = ItemPool.load_from_dataframe(items)

        estimator = MLEstimator([], item_pool.test_items)
        result = estimator.get_standard_error(0)

        self.assertAlmostEqual(result, 1.444873, 3)


class TestStandardErrorBM(unittest.TestCase):
    def test_calculation_bm(self):
        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1]
        })

        item_pool = ItemPool.load_from_dataframe(items)
        estimator = BayesModal([], item_pool.test_items, NormalPrior(0, 1))
        result = estimator.get_standard_error(0)

        self.assertAlmostEqual(result, 0.8222712, 3)

    def test_standard_error_beta(self):
        """Tests standard error calculation
        for BM and the beta distribution implemented from
        `scipy`.
        """
        items = pd.DataFrame({"a": [1.3024, 1.078, 0.8758, 0.5571, 1.225, 0.991, 0.9968, 1.1888, 1.1642, 1.1188],
                              "b": [-0.6265, 0.1836, -0.8356, 1.5953, 0.3295, -0.8205, 0.4874, 0.7383, 0.5758, -0.3054],
                              "c": [0.2052, 0.1618, 0.1957, 0.1383, 0.1324, 0.1973, 0.0058, 0.1193, 0.1831, 0.1732],
                              "d": [0.8694, 0.9653, 0.8595, 0.8112, 0.7677, 0.7749, 0.8291, 0.8797, 0.9155, 0.8517]})
        item_pool = ItemPool.load_from_dataframe(items)

        response_pattern = [0, 0, 1, 1, 1, 0, 0, 0, 0, 1]

        estimator = BayesModal(
            response_pattern,
            item_pool.test_items,
            CustomPrior(beta,
                        0.6,
                        0.9)
        )
        
        try:
            result = estimator.get_standard_error(0)
        except Exception as e:
            print(f"Standard error calculation failed due to: {e}")
        self.assertIsInstance(result, float)
        self.assertFalse(math.isnan(result))

    def test_standard_error_f(self):
        """Test for F-distribution"""
        items = pd.DataFrame({"a": [1.3024, 1.078, 0.8758, 0.5571, 1.225, 0.991, 0.9968, 1.1888, 1.1642, 1.1188],
                              "b": [-0.6265, 0.1836, -0.8356, 1.5953, 0.3295, -0.8205, 0.4874, 0.7383, 0.5758, -0.3054],
                              "c": [0.2052, 0.1618, 0.1957, 0.1383, 0.1324, 0.1973, 0.0058, 0.1193, 0.1831, 0.1732],
                              "d": [0.8694, 0.9653, 0.8595, 0.8112, 0.7677, 0.7749, 0.8291, 0.8797, 0.9155, 0.8517]})
        item_pool = ItemPool.load_from_dataframe(items)

        response_pattern = [0, 0, 1, 1, 1, 0, 0, 0, 0, 1]

        estimator = BayesModal(
            response_pattern,
            item_pool.test_items,
            CustomPrior(f,
                        20,
                        58)
        )
        
        try:
            result = estimator.get_standard_error(0)
        except Exception as e:
            print(f"Standard error calculation failed due to: {e}")
        self.assertIsInstance(result, float)
        self.assertFalse(math.isnan(result))


class TestStandardErrorEAP(unittest.TestCase):
    def test_calculations_4pl_ability_0(self):
        items = {
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1]
        }
        item_pool = ItemPool.load_from_dict(items)
        response_pattern = [0, 1, 0]
        estimator = ExpectedAPosteriori(response_pattern,
                                        item_pool.test_items,
                                        NormalPrior(0, 1),
                                        optimization_interval=(-4, 4))
        
        standard_error = estimator.get_standard_error(0)
        self.assertAlmostEqual(standard_error, 0.9866929, places=3)

    def test_standard_error_beta(self):
        """Tests standard error calculation
        for BM and the beta distribution implemented from
        `scipy`.
        """
        items = pd.DataFrame({"a": [1.3024, 1.078, 0.8758, 0.5571, 1.225, 0.991, 0.9968, 1.1888, 1.1642, 1.1188],
                              "b": [-0.6265, 0.1836, -0.8356, 1.5953, 0.3295, -0.8205, 0.4874, 0.7383, 0.5758, -0.3054],
                              "c": [0.2052, 0.1618, 0.1957, 0.1383, 0.1324, 0.1973, 0.0058, 0.1193, 0.1831, 0.1732],
                              "d": [0.8694, 0.9653, 0.8595, 0.8112, 0.7677, 0.7749, 0.8291, 0.8797, 0.9155, 0.8517]})
        item_pool = ItemPool.load_from_dataframe(items)

        response_pattern = [0, 0, 1, 1, 1, 0, 0, 0, 0, 1]

        estimator = ExpectedAPosteriori(
            response_pattern,
            item_pool.test_items,
            CustomPrior(beta,
                        0.6,
                        0.9)
        )
        
        try:
            result = estimator.get_standard_error(0)

        except Exception as e:
            print(f"Standard Error estimation failed due to: {e}")
        self.assertIsInstance(result, float)
