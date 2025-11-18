import unittest
import numpy as np
from adaptivetesting.math.estimators import EmpiricalPrior, SkewNormalPrior


class TestEmpiricalPrior(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(0)
        # univariate dataset of moderate size to avoid singular covariance
        self.dataset = self.rng.normal(loc=0.0, scale=1.0, size=200)

    def test_pdf_array_and_scalar(self):
        prior = EmpiricalPrior(self.dataset)
        points = np.array([-1.0, 0.0, 1.0])
        dens = prior.pdf(points)
        # gaussian_kde returns an array of densities for array input
        self.assertEqual(np.asarray(dens).shape[-1], points.shape[-1])
        self.assertTrue(np.all(np.asarray(dens) >= 0.0))

        # scalar input - ensure convertible to float and non-negative
        scalar_d = prior.pdf(0.0)
        scalar_val = float(np.asarray(scalar_d).ravel()[0])
        self.assertTrue(np.isfinite(scalar_val))
        self.assertGreaterEqual(scalar_val, 0.0)

    def test_pdf_peak_near_mean(self):
        prior = EmpiricalPrior(self.dataset)
        mean = float(np.mean(self.dataset))
        dens_mean = float(np.asarray(prior.pdf(np.array([mean]))).ravel()[0])
        dens_far = float(np.asarray(prior.pdf(np.array([mean + 5.0]))).ravel()[0])
        self.assertGreater(dens_mean, dens_far)


class TestSkewNormalPrior(unittest.TestCase):
    def test_pdf_scalar_and_array(self):
        prior = SkewNormalPrior(skewness=2.0, loc=0.0, scale=1.0)
        scalar = prior.pdf(0.0)
        scalar_val = float(np.asarray(scalar).ravel()[0]) if hasattr(scalar, "__array__") else float(scalar)
        self.assertTrue(np.isfinite(scalar_val))
        self.assertGreaterEqual(scalar_val, 0.0)

        arr = np.array([-3.0, 0.0, 3.0])
        dens_arr = prior.pdf(arr)
        dens_arr = np.asarray(dens_arr)
        self.assertEqual(dens_arr.shape[-1], arr.shape[-1])
        self.assertTrue(np.all(dens_arr >= 0.0))

    def test_pdf_decreases_far_from_loc(self):
        prior = SkewNormalPrior(skewness=0.0, loc=1.0, scale=0.5)
        dens_loc = float(np.asarray(prior.pdf(1.0)).ravel()[0])
        dens_far = float(np.asarray(prior.pdf(1.0 + 5.0)).ravel()[0])
        self.assertGreater(dens_loc, dens_far)


if __name__ == "__main__":
    unittest.main()
