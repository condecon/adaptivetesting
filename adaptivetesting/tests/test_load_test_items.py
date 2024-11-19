from unittest import TestCase
from ..models import TestItem, load_test_items_from_dict

class TestLoadTestItems(TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.item1 = TestItem()
        self.item1.a = 0.9
        self.item1.b = 5
        self.item1.c = 0.9

        self.item2 = TestItem()
        self.item2.a = 1.9
        self.item2.b = 3
        self.item2.c = 1.9

    def test_load_test_items_from_dict_success(self):
        source_dictionary = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
            "d": [1, 1]
        }

        generated = load_test_items_from_dict(source_dictionary)

        self.assertEqual([self.item1.__dict__(), self.item2.__dict__()], [i.__dict__() for i in generated])

    def test_load_test_items_from_dict_error_none(self):
        source_dictionary = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
        }

        with self.assertRaises(ValueError):
            load_test_items_from_dict(source_dictionary)

    def test_load_test_items_from_dict_error_length(self):
        source_dictionary = {
            "a": [0.9, 1.9],
            "b": [5, 3],
            "c": [0.9, 1.9],
            "d": [1]
        }

        with self.assertRaises(ValueError):
            load_test_items_from_dict(source_dictionary)