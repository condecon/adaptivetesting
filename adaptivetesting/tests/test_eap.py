import unittest
import pandas as pd
import numpy as np
from adaptivetesting.models import ItemPool
from adaptivetesting.math.estimators import (ExpectedAPosteriori,
                                             NormalPrior,
                                             SkewNormalPrior,
                                             EmpiricalPrior)


class TestEAP(unittest.TestCase):
    def test_estimation_4pl(self):
        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1]
        })
        item_pool = ItemPool.load_from_dataframe(items)

        response_pattern = [0, 1, 0]
        estimator = ExpectedAPosteriori(
            response_pattern=response_pattern,
            items=item_pool.test_items,
            prior=NormalPrior(0, 1),
            optimization_interval=(-4, 4)
        )

        result = estimator.get_estimation()

        self.assertAlmostEqual(result, -0.4565068, 4)


class TestSkewNormalPriorIntegration(unittest.TestCase):
    def setUp(self):
        # simple 3-item pool used elsewhere in tests
        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1.0]
        })
        self.item_pool = ItemPool.load_from_dataframe(items).test_items
        self.response_pattern = [0, 1, 0]

    def test_skewnormal_pdf_basic(self):
        prior = SkewNormalPrior(skewness=4.0, loc=0.0, scale=1.0)
        # scalar
        p0 = prior.pdf(0.0)
        self.assertTrue(np.isfinite(np.asarray(p0)).all())
        self.assertGreaterEqual(float(np.asarray(p0).ravel()[0]), 0.0)
        # array
        xs = np.array([-2.0, 0.0, 2.0])
        pa = prior.pdf(xs)
        pa = np.asarray(pa)
        self.assertEqual(pa.shape[-1], xs.shape[-1])
        self.assertTrue(np.all(pa >= 0.0))

    def test_skewnormal_changes_estimate_vs_normal(self):
        prior_norm = NormalPrior(0.0, 1.0)
        prior_skew = SkewNormalPrior(skewness=6.0, loc=0.0, scale=1.0)

        est_norm = ExpectedAPosteriori(
            response_pattern=self.response_pattern,
            items=self.item_pool,
            prior=prior_norm,
            optimization_interval=(-4, 4),
        ).get_estimation()

        est_skew = ExpectedAPosteriori(
            response_pattern=self.response_pattern,
            items=self.item_pool,
            prior=prior_skew,
            optimization_interval=(-4, 4),
        ).get_estimation()

        self.assertTrue(np.isfinite(est_norm))
        self.assertTrue(np.isfinite(est_skew))
        # skew prior should typically shift the estimate compared to symmetric prior
        self.assertNotAlmostEqual(est_norm, est_skew, places=6)


class TestEmpiricalPriorIntegration(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(0)
        self.dataset = rng.normal(loc=0.0, scale=1.0, size=300)
        self.prior = EmpiricalPrior(self.dataset)
        items = pd.DataFrame({
            "a": [1.0, 1.2, 0.9],
            "b": [0.0, 0.5, -0.5],
            "c": [0.2, 0.2, 0.2],
            "d": [1.0, 0.9, 0.95]
        })
        self.item_pool = ItemPool.load_from_dataframe(items).test_items
        self.response_pattern = [1, 0, 1]

    def test_empirical_pdf_scalar_and_array(self):
        scalar = self.prior.pdf(0.0)
        self.assertTrue(np.isfinite(np.asarray(scalar)).all())
        self.assertGreaterEqual(float(np.asarray(scalar).ravel()[0]), 0.0)

        xs = np.array([-1.0, 0.0, 1.0])
        vals = np.asarray(self.prior.pdf(xs))
        # gaussian_kde returns shape (n_points,) for 1-D data
        self.assertEqual(vals.shape[-1], xs.shape[-1])
        self.assertTrue(np.all(vals >= 0.0))

    def test_empirical_prior_works_with_ExpectedAPosteriori(self):
        estimator = ExpectedAPosteriori(
            response_pattern=self.response_pattern,
            items=self.item_pool,
            prior=self.prior,
            optimization_interval=(-4, 4),
        )
        result = estimator.get_estimation()
        self.assertTrue(np.isfinite(result))


class TestNumericalStability(unittest.TestCase):
    def setUp(self):
        # moderate 4PL pool for stability checks
        self.items = pd.DataFrame({
            "a": [1.3024, 1.078, 0.8758, 0.5571],
            "b": [-0.6265, 0.1836, -0.8356, 1.5953],
            "c": [0.2052, 0.1618, 0.1957, 0.1383],
            "d": [0.8694, 0.9653, 0.8595, 0.8112]
        })
        self.item_pool = ItemPool.load_from_dataframe(self.items).test_items

    def test_tight_normal_prior_keeps_estimate_near_mean(self):
        # extremely tight prior around mean 2.0 should pull estimate close to 2.0
        prior = NormalPrior(mean=2.0, sd=1e-6)
        responses = [1, 1, 1, 1]  # all-correct
        estimator = ExpectedAPosteriori(
            response_pattern=responses,
            items=self.item_pool,
            prior=prior,
            optimization_interval=(-10, 10),
        )
        result = estimator.get_estimation()
        self.assertTrue(np.isfinite(result))
        # result should be extremely close to the prior mean
        self.assertAlmostEqual(result, 2.0, delta=0.1)

    def test_extreme_response_patterns_do_not_crash(self):
        # all incorrect
        prior = NormalPrior(0.0, 1.0)
        for responses in ([0, 0, 0, 0], [1, 1, 1, 1]):
            estimator = ExpectedAPosteriori(
                response_pattern=responses,
                items=self.item_pool,
                prior=prior,
                optimization_interval=(-10, 10),
            )
            result = estimator.get_estimation()
            self.assertTrue(np.isfinite(result))
            # result lies within the provided optimization interval
            self.assertGreaterEqual(result, -10)
            self.assertLessEqual(result, 10)
