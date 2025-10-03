import unittest
import adaptivetesting as adt
import pandas as pd


class TestMaximumPriorityIndex(unittest.TestCase):
    def __init__(self, methodName="runTest"):

        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1],
            "id": [1, 2, 3]
        })

        self.available_items = adt.ItemPool.load_from_dataframe(items).test_items
        self.content_categories = ["Math", "English", "Math"]
        
        for i, _ in enumerate(self.available_items):
            self.available_items[i].additional_properties = {
                "category": [self.content_categories[i]]
            }

        super().__init__(methodName)

    def test_basic_calculation(self):
        adt.compute_priority_index(
            item=self.available_items[0],
            group_weights={
                "Math": 0.2,
                "English": 0.8
            },
            required_items=10,
            shown_item=0,
            current_ability=0
        )

    def test_quota_calculation(self):
        result = adt.compute_quota_left(10, 5)
        self.assertAlmostEqual(result, 0.5)
    
    def test_exception_list(self):
        with self.assertRaises(adt.ItemSelectionException):
            self.available_items[0].additional_properties["category"] = 0
            adt.compute_priority_index(
                item=self.available_items[0],
                group_weights={
                    "Math": 0.2,
                    "English": 0.8
                },
                required_items=10,
                shown_item=0,
                current_ability=0
            )

    def test_exception_key(self):
        with self.assertRaises(adt.ItemSelectionException):
            self.available_items[0].additional_properties.pop("category")
            adt.compute_priority_index(
                item=self.available_items[0],
                group_weights={
                    "Math": 0.2,
                    "English": 0.8
                },
                required_items=10,
                shown_item=0,
                current_ability=0
            )
