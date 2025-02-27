import unittest
from typing import List
from adaptivetesting.math import standard_error
from adaptivetesting.models import ItemPool, TestItem

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
