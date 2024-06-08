import unittest
from adaptivetesting.math import standard_error

class TestStandardError(unittest.TestCase):
    def test_dummy_items(self):
        items = [0.7, 0.9, 0.6]
        ability = 0

        result = standard_error(items, ability)

        self.assertAlmostEqual(result, 1.234664423, 3)

    def test_eid_items(self):
        items = [-1.603, 0.909]
        ability = -0.347

        result = standard_error(items, ability)

        self.assertAlmostEqual(result, 1.702372, 3)
