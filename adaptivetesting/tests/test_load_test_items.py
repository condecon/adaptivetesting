from unittest import TestCase
from adaptivetesting.models import TestItem, ItemPool
import pandas as pd


class TestLoadTestItems(TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.item1 = TestItem()
        self.item1.a = 0.9
        self.item1.b = 5
        self.item1.c = 0.9

        self.item2 = TestItem()
        self.item2.a = 1.9
        self.item2.b = 3
        self.item2.c = 1.9
# List

# Dict
    def test_load_test_items_from_dict_success(self):
        source_dictionary: dict[str, list[float]] = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
            "d": [1, 1]
        }

        generated = ItemPool.load_from_dict(source_dictionary)

        self.assertEqual([self.item1.as_dict(), self.item2.as_dict()], [i.as_dict() for i in generated.test_items])

    def test_load_test_items_from_dict_error_none(self):
        source_dictionary: dict[str, list[float]] = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
        }

        with self.assertRaises(ValueError):
            ItemPool.load_from_dict(source_dictionary)

    def test_load_test_items_from_dict_error_length(self):
        source_dictionary: dict[str, list[float]] = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
            "d": [1]
        }

        with self.assertRaises(ValueError):
            ItemPool.load_from_dict(source_dictionary)

# Pandas DataFrame
    def test_load_items_from_pandas_success(self):
        dictionary = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
            "d": [1, 1],
            "simulated_responses": [1, 0]
        }
        df = pd.DataFrame(dictionary)

        generated = ItemPool.load_from_dataframe(df)

        # check that items are equal
        self.assertEqual(
            {
                "a": 0.9,
                "b": 5,
                "c": 0.9,
                "d": 1
            },
            generated.test_items[0].as_dict()
        )

        self.assertEqual(
            {
                "a": 1.9,
                "b": 3,
                "c": 1.9,
                "d": 1
            },
            generated.test_items[1].as_dict()
        )

        self.assertEqual([1, 0], generated.simulated_responses)
        
    def test_load_items_pandas_error_missing_column(self):
        dictionary = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9]
        }
        df = pd.DataFrame(dictionary)

        with self.assertRaises(ValueError):
            ItemPool.load_from_dataframe(df)

    def test_load_pandas_no_responses(self):
        dictionary = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
            "d": [1, 1]
        }
        df = pd.DataFrame(dictionary)

        generated = ItemPool.load_from_dataframe(df)

        self.assertIsNone(generated.simulated_responses)
