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

        self.item1_with_id = TestItem()
        self.item1_with_id.a = self.item1.a
        self.item1_with_id.b = self.item1.b
        self.item1_with_id.c = self.item1.c
        self.item1_with_id.id = 1

        self.item2_with_id = TestItem()
        self.item2_with_id.a = self.item2.a
        self.item2_with_id.b = self.item2.b
        self.item2_with_id.c = self.item2.c
        self.item2_with_id.id = 42
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

    def test_load_test_items_from_dict_with_id_success(self):
        source_dictionary: dict[str, list[float]] = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
            "d": [1, 1],
            "id": [1, 42]
        }

        generated = ItemPool.load_from_dict(source_dictionary)

        self.assertEqual([self.item1_with_id.as_dict(), self.item2_with_id.as_dict()], [i.as_dict()
                         for i in generated.test_items])

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
                "d": 1,
                "additional_properties": {},
                "id": None
            },
            generated.test_items[0].as_dict()
        )

        self.assertEqual(
            {
                "a": 1.9,
                "b": 3,
                "c": 1.9,
                "d": 1,
                "additional_properties": {},
                "id": None
            },
            generated.test_items[1].as_dict()
        )

        self.assertEqual([1, 0], generated.simulated_responses)

    def test_load_items_from_pandas_with_ids_success(self):
        dictionary = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
            "d": [1, 1],
            "simulated_responses": [1, 0],
            "ids": [101, 202]
        }
        df = pd.DataFrame(dictionary)

        generated = ItemPool.load_from_dataframe(df)

        # check that items are equal
        self.assertEqual(
            {
                "a": 0.9,
                "b": 5,
                "c": 0.9,
                "d": 1,
                "id": 101,
                "additional_properties": {}
            },
            generated.test_items[0].as_dict(with_id=True)
        )

        self.assertEqual(
            {
                "a": 1.9,
                "b": 3,
                "c": 1.9,
                "d": 1,
                "id": 202,
                "additional_properties": {}
            },
            generated.test_items[1].as_dict(with_id=True)
        )

        self.assertEqual([1, 0], generated.simulated_responses)

    def test_load_items_pandas_error_missing_column(self):
        dictionary = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9]
        }
        df = pd.DataFrame(dictionary)
        # this should work because d can be ignored when creating items
        pool = ItemPool.load_from_dataframe(df)
        # check that the pool contains the correct items
        item1 = TestItem()
        item1.a = 0.9
        item1.b = 5
        item1.c = 0.9
        item1.d = 1

        item2 = TestItem()
        item2.a = 1.9
        item2.b = 3
        item2.c = 1.9
        item2.d = 1

        self.assertDictEqual(item1.as_dict(), pool.test_items[0].as_dict())
        self.assertDictEqual(item2.as_dict(), pool.test_items[1].as_dict())

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

    def test_load_dict_content_balancing(self):
        source_dictionary: dict[str, list[float]] = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
            "d": [1, 1]
        }

        item_pool = ItemPool.load_from_dict(source=source_dictionary,
                                            content_categories=[["math"], ["english"]])
        items = item_pool.test_items
        assigned_groups = [item.additional_properties["category"] for item in items]

        self.assertListEqual(assigned_groups, [["math"], ["english"]])

    def test_load_list_content_balancing(self):
        source_dictionary: dict[str, list[float] | list[int] | list[list[str]]] = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
            "d": [1, 1],
            "group": [["math"], ["english"]]
        }

        item_pool = ItemPool.load_from_list(
            a=source_dictionary["a"], # type: ignore
            b=source_dictionary["b"], # type: ignore
            c=source_dictionary["c"], # type: ignore
            d=source_dictionary["d"], # type: ignore
            content_categories=source_dictionary["group"] # type: ignore
        )
        items = item_pool.test_items
        assigned_groups = [item.additional_properties["category"] for item in items]

        self.assertListEqual(assigned_groups, [["math"], ["english"]])

    def test_load_dataframe_content_balancing(self):
        source_dictionary: dict[str, list[float] | list[int] | list[list[str]]] = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
            "d": [1, 1],
            "content_categories": [["math"], ["english"]]
        }

        item_pool = ItemPool.load_from_dataframe(pd.DataFrame(source_dictionary))
        items = item_pool.test_items
        assigned_groups = [item.additional_properties["category"] for item in items]

        self.assertListEqual(assigned_groups, [["math"], ["english"]])


class TestTestItemRoundTrip(TestCase):
    def test_roundtrip_preserves_fields(self):
        # create and populate original item
        original = TestItem()
        original.id = 42
        original.a = 1.2
        original.b = -0.5
        original.c = 0.25
        original.d = 0.95
        original.additional_properties = {
            "category": ["Math", "Science"],
            "meta": {"difficulty": "hard", "tags": ["algebra", "geometry"]},
        }

        # serialize including id
        data_with_id = original.as_dict()

        # deserialize
        restored = TestItem.from_dict(data_with_id)

        # verify fields preserved
        self.assertEqual(restored.id, original.id)
        self.assertEqual(restored.a, original.a)
        self.assertEqual(restored.b, original.b)
        self.assertEqual(restored.c, original.c)
        self.assertEqual(restored.d, original.d)
        self.assertEqual(restored.additional_properties, original.additional_properties)


class TestPolyItems(TestCase):
    def test_loading_items_list(self):
        items = ItemPool.load_from_list(
            a = [0.934, 0.972, 1.210],
            b = [
                [0.071, 0.129],
                [1.715, 0.461],
                [-1.265, -0.687]
            ]
        ).test_items

        self.assertTrue(all([isinstance(item.a, float) for item in items]))
        self.assertTrue(all([isinstance(item.b, list) for item in items]))

    def test_loading_items_dict(self):
        items_dict = {
            "a" : [0.934, 0.972, 1.210],
            "b": [
                [0.071, 0.129],
                [1.715, 0.461],
                [-1.265, -0.687]
            ]
        }
        
        items = ItemPool.load_from_dict(
            items_dict
        ).test_items

        self.assertTrue(all([isinstance(item.a, float) for item in items]))
        self.assertTrue(all([isinstance(item.b, list) for item in items]))

    def test_loading_items_df(self):
        items_dict = {
            "a" : [0.934, 0.972, 1.210],
            "b": [
                [0.071, 0.129],
                [1.715, 0.461],
                [-1.265, -0.687]
            ]
        }

        df = pd.DataFrame(items_dict)
        items = ItemPool.load_from_dataframe(df).test_items

        self.assertTrue(all([isinstance(item.a, float) for item in items]))
        self.assertTrue(all([isinstance(item.b, list) for item in items]))
