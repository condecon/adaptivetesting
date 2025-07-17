import unittest
from adaptivetesting.models import AdaptiveTest, TestItem, ItemPool
from adaptivetesting.math.estimators import MLEstimator
from adaptivetesting.math.item_selection import urrys_rule

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
simulated_responses = [1, 0, 1]

item_pool = ItemPool(
    test_items=items.copy(),
    simulated_responses=simulated_responses.copy()
)


class TestAdaptiveTest(unittest.TestCase, AdaptiveTest):
    def __init__(self, methodName='runTest'):
        AdaptiveTest.__init__(
            self,
            item_pool=item_pool,
            simulation_id="1",
            true_ability_level=0,
            participant_id="0"
        )
        unittest.TestCase.__init__(self, methodName)
    
    def get_next_item(self):
        return urrys_rule(self.item_pool.test_items, self.ability_level)

    def estimate_ability_level(self) -> tuple[float, float]:
        return 0, float("NaN")

    def test_get_difficulties(self):
        difficulties = self.get_item_difficulties()
        self.assertEqual(difficulties, [0.24, 0.89, -0.6])

    def test_standard_error(self):
        """This should calculate a standard error without failing"""
        self.answered_items = [item1, item2]
        response_pattern: list[int] = []
        estimator = MLEstimator(response_pattern, self.answered_items)
        estimator.get_standard_error(0)

    def test_get_next_item(self):
        next_item = self.get_next_item()
        self.assertDictEqual(next_item.as_dict(), item1.as_dict())

    def test_testing_procedure_once(self):
        self.run_test_once()
        # test showed item
        self.assertEqual(self.test_results[0].showed_item,
                         item1.as_dict())

        # print(self.test_results)
        # print(simulated_responses)
        # test response
        self.assertEqual(
            self.test_results[0].response,
            simulated_responses[0]
        )

        # test item is removed from pool
        # print(self.item_pool.test_items)
        self.assertListEqual([item.as_dict() for item in self.item_pool.test_items], [item2.as_dict(), item3.as_dict()])
