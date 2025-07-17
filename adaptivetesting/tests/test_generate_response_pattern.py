# flake8: noqa
import unittest
from adaptivetesting.models import ItemPool
from adaptivetesting.math.estimators import MLEstimator
from adaptivetesting.math import generate_response_pattern


source_dictionary = {"a": [1.0507,
                           0.9943,
                           0.9914,
                           1.2737,
                           0.9548,
                           1.3033,
                           0.6902,
                           1.1169,
                           1.0248,
                           1.0432,
                           1.0759,
                           0.8995,
                           0.9334,
                           0.7963,
                           0.7856,
                           1.0607,
                           1.0896,
                           1.0106,
                           1.1845,
                           1.41,
                           0.9018,
                           0.5382,
                           1.2011,
                           0.8582,
                           0.8624, 1.2051, 0.943, 0.7559, 1.0363, 0.9722, 1.0012, 1.0771, 0.9259, 1.1289, 0.9559, 1.0664, 1.2194, 1.087, 0.9348, 1.2298, 1.1987, 1.1097, 1.0477, 0.8744, 1.2721, 0.8799, 1.4375, 1.3065, 0.9529, 0.7947],
                     "b":
                     [-0.5605, -0.2302, 1.5587, 0.0705, 0.1293, 1.7151, 0.4609, -1.2651, -0.6869, -0.4457, 1.2241, 0.3598, 0.4008, 0.1107, -0.5558, 1.7869, 0.4979, -1.9666, 0.7014, -0.4728, -1.0678, -0.218, -1.026, -0.7289, -0.625, -1.6867, 0.8378, 0.1534, -1.1381, 1.2538, 0.4265, -0.2951, 0.8951, 0.8781, 0.8216, 0.6886, 0.5539, -0.0619, -0.306, -0.3805, -0.6947, -0.2079, -1.2654, 2.169, 1.208, -1.1231, -
                      0.4029, -0.4667, 0.78, -0.0834], "c": [0.0597, 0.2406, 0.1503, 0.1288, 0.1006, 0.2201, 0.091, 0.0721, 0.0427, 0.043, 0.1205, 0.0632, 0.0541, 0.1686, 0.0119, 0.1752, 0.088, 0.1022, 0.2052, 0.2297, 0.0706, 0.2403, 0.1821, 0.1716, 0.0132, 0.0988, 0.1195, 0.1401, 0.1746, 0.2289, 0.1546, 0.1071, 0.1355, 0.0146, 0.0652, 0.0993, 0.0494, 0.208, 0.0382, 0.2009, 0.1367, 0.1656, 0.0429, 0.1583, 0.078, 0.1811, 0.0997, 0.2423, 0.2418, 0.1817], "d": [0.8143, 0.8054, 0.8983, 0.8169, 0.8828, 0.9463, 0.792, 0.8511, 0.8679, 0.967, 0.9814, 0.9705, 0.9185, 0.9875, 0.8791, 0.8941, 0.8341, 0.8368, 0.755, 0.8757, 0.9678, 0.7516, 0.768, 0.7911, 0.9426, 0.9338, 0.993, 0.8666, 0.7686, 0.9122, 0.9396, 0.7843, 0.8491, 0.8062, 0.7645, 0.849, 0.7662, 0.8065, 0.7637, 0.9176, 0.8244, 0.7752, 0.768, 0.9701, 0.9386, 0.9542, 0.9955, 0.7759, 0.7748, 0.9497]}


class TestGenerateResponsePattern(unittest.TestCase):
    def test_generate_pattern_and_not_break(self):
        item_pool = ItemPool.load_from_dict(source_dictionary)

        # generate pattern
        responses = generate_response_pattern(0, item_pool.test_items, seed=1234)
        compare_respones = [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1,
                            1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1]

        self.assertListEqual(responses, compare_respones)

    def test_compare_generation_to_etsimation(self):
        item_pool = ItemPool.load_from_dict(source_dictionary)

        # generate pattern
        responses = generate_response_pattern(0, item_pool.test_items, seed=5000)

        # estimate
        estimator = MLEstimator(responses, item_pool.test_items)
        estimation = estimator.get_estimation()

        self.assertAlmostEqual(estimation, 0, places=1)
