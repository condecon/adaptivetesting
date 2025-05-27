import unittest
from adaptivetesting.math import test_information_function, generate_response_pattern
from adaptivetesting.models import ItemPool
import jax.numpy as np
import pandas as pd
import math


class TestInformation(unittest.TestCase):
    def test_information_calculation_1pl(self):
        difficulties = np.array([-0.6265,0.1836,-0.8356])
        ability = np.array([0], dtype="float32")
        # convert difficulties into items
        item_pool = ItemPool.load_from_list(b=difficulties)
        # generate response pattern
        response_pattern = np.array(generate_response_pattern(
            ability,
            item_pool.test_items,
            1234
        ))

        result = test_information_function(
            mu=ability,
            a=np.array(1),
            b=difficulties,
            c=np.array(0),
            d=np.array(1),
            response_pattern=np.array(response_pattern)
        )


        self.assertAlmostEqual(result, 0.4704, 3)

    def test_information_calculation_4pl(self):
        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1]
        })

        item_pool = ItemPool.load_from_dict(items)
        response_pattern = generate_response_pattern(0, item_pool.test_items, 1234)

        result = test_information_function(np.array(0),
                                           np.array(items.a.to_numpy()),
                                           np.array(items.b.to_numpy()),
                                           np.array(items.c.to_numpy()),
                                           np.array(items.d.to_numpy()),
                                           np.array(response_pattern))
        # convert test information into standard error
        result = 1 / math.sqrt(result)

        self.assertAlmostEqual(result, 1.444873, 3)
