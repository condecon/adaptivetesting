import unittest
from ..models.adaptive_test import AdaptiveTest
from ..models.test_item import TestItem


class TestAdaptiveTest(unittest.TestCase, AdaptiveTest):
    item1 = TestItem()
    item1.b = 0.24
    item1.id = 1
    item1.simulated_response = 1

    item2 = TestItem()
    item2.b = 0.89
    item2.id = 2
    item2.simulated_response = 0

    item3 = TestItem()
    item3.b = -0.6
    item3.id = 3
    item3.simulated_response = 1

    items = [item1, item2, item3]

    def __init__(self, methodName = "runTest"):
        AdaptiveTest.__init__(
            self,
            items=self.items,
            participant_id=0,
            simulation_id="1",
            true_ability_level=0
        )
        unittest.TestCase.__init__(self, methodName)

    def estimate_ability_level(self, answered_items_difficulties: list[float]) -> float:
        return 0

    def test_get_difficulties(self):
        difficulties = self.get_item_difficulties()
        self.assertEqual(difficulties, [0.24, 0.89, -0.6])

    def test_standard_error(self):
        """This should calculate a standard error without failing"""
        self.answered_items = [self.item1, self.item2]
        error = self.get_ability_se()

    def test_get_next_item(self):
        next_item = self.get_next_item()
        self.assertEqual(next_item, self.item1)

    def test_testing_procedure_once(self):
        self.run_test_once()
        # test showed item
        self.assertEqual(self.test_results[0].showed_item,
                         self.item1.b)
        # test response
        self.assertEqual(
            self.test_results[0].response,
            self.item1.simulated_response
        )

        # test item is removed from pool
        print(self.items)
        self.assertEqual(self.items, [self.item2, self.item3])

