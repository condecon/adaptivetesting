import unittest
from typing import List
from adaptivetesting.math import standard_error
from adaptivetesting.models import ItemPool, TestItem
import pandas as pd


class TestStandardError(unittest.TestCase):
    def test_dummy_items(self):
        items = [0.7, 0.9, 0.6]
        ability = 0

        item_list: List[TestItem] = ItemPool.load_from_list(items).test_items

        result = standard_error(item_list, ability)

        self.assertAlmostEqual(result, 1.234664423, 3)

    def test_eid_items(self):
        items = [-1.603, 0.909]
        ability = -0.347

        item_list = ItemPool.load_from_list(items).test_items

        result = standard_error(item_list, ability)

        self.assertAlmostEqual(result, 1.702372, 3)

    def test_calculation_4pl(self):
        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1]
        })

        item_pool = ItemPool.load_from_dataframe(items)

        result = standard_error(item_pool.test_items, 0)

        self.assertAlmostEqual(result, 1.444873, 3)

    def test_calculation_bm(self):
        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1]
        })

        item_pool = ItemPool.load_from_dataframe(items)

        result = standard_error(item_pool.test_items,
                                0,
                                estimator="BM",
                                sd=1)

        self.assertAlmostEqual(result, 0.8222712, 3)
