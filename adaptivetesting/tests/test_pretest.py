import unittest
from adaptivetesting.implementations import PreTest
from adaptivetesting.models import TestItem
import jax.numpy as np

item0 = TestItem()
item0.b = 0

item1 = TestItem()
item1.b = 0.2

item2 = TestItem()
item2.b = 0.4

item3 = TestItem()
item3.b = 0.6

item4 = TestItem()
item4.b = 0.8

items = [item0, item1, item2, item3, item4]

test = PreTest(
    items=items
)
# a seed is not set because
# the random selection should only allow one solution


class TestPreTest(unittest.TestCase):
    def test_quantile_calculation(self):
        quantiles: np.ndarray = test.calculate_quantiles()
        quantiles = quantiles.round(decimals=1)
        self.assertListEqual(list(quantiles), [0.2, 0.4, 0.6])
    
    def test_selection_random_item_quantile(self):
        selected_items = test.select_random_item_quantile()
        self.assertListEqual(selected_items,
                             [item1, item2, item3, item4])
