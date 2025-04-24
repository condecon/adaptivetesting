import unittest
from adaptivetesting.math import test_information_function
import jax.numpy as np
import pandas as pd
import math


class TestInformation(unittest.TestCase):
    def test_information_calculation_1pl(self):
        difficulties = np.array([0.7, 0.9, 0.6])
        ability = np.array([0], dtype="float32")

        result = test_information_function(
            mu=ability,
            a=np.array(1),
            b=difficulties,
            c=np.array(1),
            d=np.array(0),
        )

        self.assertAlmostEqual(result, 0.6559974211, 3)

    def test_information_calculation_4pl(self):
        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1]
        })

        result = test_information_function(np.array(0),
                                           np.array(items.a.to_numpy()),
                                           np.array(items.b.to_numpy()),
                                           np.array(items.c.to_numpy()),
                                           np.array(items.d.to_numpy()))
        # convert test information into standard error
        result = 1 / math.sqrt(result)

        self.assertAlmostEqual(result, 1.444873, 3)
