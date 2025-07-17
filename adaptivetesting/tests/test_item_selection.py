import unittest
from adaptivetesting.math.item_selection import urrys_rule, maximum_information_criterion
from adaptivetesting.models import TestItem, ItemPool


# unittests for urrys rule
class TestUrrysRule(unittest.TestCase):
    item1 = TestItem()
    item1.b = 0.24
    item1.id = 1

    item2 = TestItem()
    item2.b = 0.89
    item2.id = 2

    item3 = TestItem()
    item3.b = -0.6
    item3.id = 3

    items = [item1, item2, item3]

    def test_selection_when_0(self):
        ability_level = 0

        self.assertEqual(urrys_rule(self.items, ability_level).id, 1)

    def test_selection_when_minus_0_5(self):
        ability_level = -0.5
        self.assertEqual(urrys_rule(self.items, ability_level).id, 3)


# unittests for the maximum information criterion
class TestMaximumInformationCriterion(unittest.TestCase):
    def load_items(self) -> list[TestItem]:
        item_dict = {
            "a": [0.8359, 1.0975, 1.1477, 1.1152, 0.9389],
            "b": [-0.6265, 0.1836, -0.8356, 1.5953, 0.3295],
            "c": [0.2337, 0.053, 0.1629, 0.0314, 0.0668],
            "d": [0.8465, 0.7533, 0.8456, 0.9674, 0.8351]}
        
        item_pool = ItemPool.load_from_dict(item_dict)
        return item_pool.test_items
    
    def test_selection_when_0(self):
        items = self.load_items()
        selected_item = maximum_information_criterion(
            items,
            0
        )
        self.assertDictEqual(selected_item.as_dict(),
                             {"a": 1.0975, "b": 0.1836, "c": 0.053, "d": 0.7533})
        
    def test_selection_when_minus_0_5(self):
        items = self.load_items()
        selected_item = maximum_information_criterion(
            items,
            -0.5
        )
        self.assertDictEqual(selected_item.as_dict(),
                             {"a": 1.1477, "b": -0.8356, "c": 0.1629, "d": 0.8456})
