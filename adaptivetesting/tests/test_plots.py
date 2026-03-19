# type: ignore
import unittest
from unittest.mock import patch
from adaptivetesting.utils import (
    plot_final_ability_estimates,
    plot_icc,
    plot_iif,
    plot_exposure_rate,
    plot_test_information,
    plot_theta_estimation_trace
)
from adaptivetesting.models.__test_item import TestItem
from adaptivetesting.models.__misc import ResultOutputFormat
import matplotlib


class TestPlots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dummy_item = TestItem()
        cls.dummy_item.id = 1
        cls.dummy_item.a = 1.0
        cls.dummy_item.b = 0.0
        cls.dummy_item.c = 0.2
        cls.dummy_item.d = 1.0
        cls.dummy_items = [cls.dummy_item for _ in range(3)]
        cls.simulation_id = 'sim1'
        cls.participant_ids = ['p1', 'p2']
        cls.output_format = ResultOutputFormat.CSV

    @patch('adaptivetesting.utils.__plots.load_final_test_results')
    def test_plot_final_ability_estimates(self, mock_load):
        # Mock return value: list of objects with .ability_estimation and .true_ability_level
        class DummyResult:
            def __init__(self, est, true):
                self.ability_estimation = est
                self.true_ability_level = true
        mock_load.return_value = [DummyResult(1.0, 1.2), DummyResult(0.5, 0.7)]
        fig, ax = plot_final_ability_estimates(
            self.simulation_id,
            self.participant_ids,
            self.output_format
        )
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsNotNone(ax)

    def test_plot_icc(self):
        fig, ax = plot_icc(self.dummy_item)
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsNotNone(ax)

    def test_plot_iif(self):
        fig, ax = plot_iif(self.dummy_item)
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsNotNone(ax)

    @patch('adaptivetesting.utils.__plots.load_test_results_single_participant')
    def test_plot_exposure_rate(self, mock_load):
        # Mock return value: list of objects with .showed_item["id"]
        class DummyResult:
            def __init__(self, item_id):
                self.showed_item = {"id": item_id}
        mock_load.return_value = [
            DummyResult("item1"), DummyResult("item2")
        ]
        fig, ax = plot_exposure_rate(
            self.simulation_id,
            self.participant_ids,
            self.output_format
        )
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsNotNone(ax)

    def test_plot_test_information(self):
        fig, ax = plot_test_information(self.dummy_items)
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsNotNone(ax)

    @patch('adaptivetesting.utils.__plots.load_test_results_single_participant')
    def test_plot_theta_estimation_trace(self, mock_load):
        # Mock return value: list of objects with .true_ability_level and .ability_estimation
        class DummyResult:
            def __init__(self, true, est):
                self.true_ability_level = true
                self.ability_estimation = est
        mock_load.return_value = [DummyResult(1.0, 0.9), DummyResult(1.2, 1.1)]
        fig, ax = plot_theta_estimation_trace(
            self.simulation_id,
            self.participant_ids[0],
            self.output_format
        )
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsNotNone(ax)


if __name__ == "__main__":
    unittest.main()
