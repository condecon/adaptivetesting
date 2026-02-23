import unittest
import numpy as np

from adaptivetesting.math.__gen_response_pattern import generate_response_pattern
from adaptivetesting.models.__test_item import TestItem


def make_dichotomous_item(a=1.0, b=0.0, c=0.0, d=1.0):
    it = TestItem()
    it.a = a
    it.b = b
    it.c = c
    it.d = d
    return it


def make_polyt_item(a=1.0, b_list=None):
    it = TestItem()
    it.a = a
    it.b = b_list if b_list is not None else [-1.0, 0.0]
    it.c = 0.0
    it.d = 1.0
    return it


class TestGenerateResponsePattern(unittest.TestCase):
    def test_dichotomous_reproducible_seed(self):
        items = [make_dichotomous_item() for _ in range(5)]
        r1 = generate_response_pattern(ability=0.0, items=items, seed=123)
        r2 = generate_response_pattern(ability=0.0, items=items, seed=123)
        self.assertEqual(r1, r2)
        self.assertEqual(len(r1), len(items))
        for x in r1:
            self.assertIsInstance(x, int)
            self.assertIn(x, (0, 1))

    def test_polytomous_requires_model(self):
        items = [make_polyt_item() for _ in range(3)]
        with self.assertRaises(ValueError):
            generate_response_pattern(ability=0.0, items=items, model=None, seed=1)

    def test_polytomous_one_hot_and_reproducible(self):
        items = [make_polyt_item(b_list=[-1.0, 0.0, 1.0]) for _ in range(4)]
        r1 = generate_response_pattern(ability=0.5, items=items, model="GRM", seed=42)
        r2 = generate_response_pattern(ability=0.5, items=items, model="GRM", seed=42)

        self.assertEqual(len(r1), len(items))

        for a, b in zip(r1, r2):
            self.assertTrue(np.array_equal(np.asarray(a), np.asarray(b)))

        for resp in r1:
            arr = np.asarray(resp)
            self.assertTrue(np.issubdtype(arr.dtype, np.integer))
            self.assertEqual(arr.ndim, 1)
            self.assertEqual(int(arr.sum()), 1)
            self.assertTrue(set(arr.flatten()).issubset({0, 1}))


if __name__ == "__main__":
    unittest.main()
