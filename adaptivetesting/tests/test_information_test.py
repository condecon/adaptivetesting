import unittest
from adaptivetesting.math.estimators import NormalPrior, test_information_function, prior_information_function
import numpy as np
import pandas as pd
import math


class TestTestInformation(unittest.TestCase):
    def test_information_calculation_1pl(self):
        difficulties = [-0.6265, 0.1836, -0.8356]
        ability = np.array([0], dtype="float32")

        result = test_information_function(
            mu=ability,
            a=np.array(1),
            b=np.array(difficulties),
            c=np.array(0),
            d=np.array(1)
        )

        self.assertAlmostEqual(result, 0.6859, 3)

    def test_information_calculation_4pl(self):
        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1]
        })

        result = test_information_function(np.array(0, dtype=float),
                                           np.array(items.a.to_numpy()),
                                           np.array(items.b.to_numpy()),
                                           np.array(items.c.to_numpy()),
                                           np.array(items.d.to_numpy()))
        # convert test information into standard error
        result = 1 / math.sqrt(result)

        self.assertAlmostEqual(result, 1.444873, 3)


class TestPriorInformation(unittest.TestCase):
    def test_normal_prior_variance(self):
        # since the information of a normal distribution
        # is 1 / variance, this should also be the result
        # of the prior_information_function
        prior = NormalPrior(0, 1)
        prior_variance = prior.sd ** 2

        # use prior information function
        estimated_prior_information = prior_information_function(
            prior=prior
        )

        self.assertAlmostEqual(float(estimated_prior_information), 1 / prior_variance, places=3)
