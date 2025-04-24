import unittest
from adaptivetesting.math.item_selection import urrys_rule
from adaptivetesting.models import TestItem


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
