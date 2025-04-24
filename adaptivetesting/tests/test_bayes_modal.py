import unittest
from adaptivetesting.models import ItemPool
from adaptivetesting.math.estimators import BayesModal, NormalPrior
import pandas as pd


class TestBayesModal(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_estimation_4pl(self):
        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1]
        })
        item_pool = ItemPool.load_from_dataframe(items)

        response_pattern = [0, 1, 0]
        estimator = BayesModal(
            response_pattern=response_pattern,
            items=item_pool.test_items,
            prior=NormalPrior(0, 1),
            optimization_interval=(-4, 4)
        )

        result = estimator.get_estimation()

        self.assertAlmostEqual(result, -0.4741753, 4)
