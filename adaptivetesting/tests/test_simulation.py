import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from adaptivetesting.simulation.__simulation import Simulation
from adaptivetesting.models.__adaptive_test import AdaptiveTest
from adaptivetesting.models.__misc import ResultOutputFormat, StoppingCriterion


def get_mock_adaptive_test():
    mock_test = MagicMock(spec=AdaptiveTest)
    mock_test.simulation_id = "sim1"
    mock_test.participant_id = "p1"
    mock_test.test_results = {"score": 42}
    # Properly mock item_pool and its test_items
    mock_item_pool = MagicMock()
    type(mock_item_pool).test_items = PropertyMock(return_value=[1, 2, 3])
    mock_test.item_pool = mock_item_pool
    mock_test.check_se_criterion.return_value = False
    mock_test.check_length_criterion.return_value = False
    mock_test.run_test_once = MagicMock()
    return mock_test


def get_mock_adaptive_test_empty_pool():
    mock_test = MagicMock(spec=AdaptiveTest)
    mock_test.simulation_id = "sim2"
    mock_test.participant_id = "p2"
    mock_test.test_results = {"score": 99}
    mock_item_pool = MagicMock()
    type(mock_item_pool).test_items = PropertyMock(return_value=[])
    mock_test.item_pool = mock_item_pool
    mock_test.run_test_once = MagicMock()
    return mock_test


class TestSimulation(unittest.TestCase):

    @patch("adaptivetesting.simulation.__simulation.PickleContext")
    @patch("adaptivetesting.simulation.__simulation.CSVContext")
    def test_save_test_results_pickle(self, mock_csv, mock_pickle):
        mock_adaptive_test = get_mock_adaptive_test()
        sim = Simulation(test=mock_adaptive_test, test_result_output=ResultOutputFormat.PICKLE)
        sim.save_test_results()
        mock_pickle.assert_called_once_with(simulation_id="sim1", participant_id="p1")
        mock_pickle.return_value.save.assert_called_once_with({"score": 42})
        mock_csv.assert_not_called()

    @patch("adaptivetesting.simulation.__simulation.PickleContext")
    @patch("adaptivetesting.simulation.__simulation.CSVContext")
    def test_save_test_results_csv(self, mock_csv, mock_pickle):
        mock_adaptive_test = get_mock_adaptive_test()
        sim = Simulation(test=mock_adaptive_test, test_result_output=ResultOutputFormat.CSV)
        sim.save_test_results()
        mock_csv.assert_called_once_with(simulation_id="sim1", participant_id="p1")
        mock_csv.return_value.save.assert_called_once_with({"score": 42})
        mock_pickle.assert_not_called()

    def test_simulate_stops_on_empty_pool(self):
        mock_adaptive_test_empty_pool = get_mock_adaptive_test_empty_pool()
        sim = Simulation(test=mock_adaptive_test_empty_pool, test_result_output=ResultOutputFormat.CSV)
        sim.simulate()
        self.assertEqual(mock_adaptive_test_empty_pool.run_test_once.call_count, 1)

    def test_simulate_stops_on_se_criterion(self):
        mock_adaptive_test = get_mock_adaptive_test()
        mock_adaptive_test.item_pool.test_items = [1]
        mock_adaptive_test.check_se_criterion.side_effect = [True]
        sim = Simulation(test=mock_adaptive_test, test_result_output=ResultOutputFormat.CSV)
        sim.simulate(criterion=StoppingCriterion.SE, value=0.9)
        self.assertEqual(mock_adaptive_test.run_test_once.call_count, 1)

    def test_simulate_stops_on_length_criterion(self):
        mock_adaptive_test = get_mock_adaptive_test()
        mock_adaptive_test.item_pool.test_items = [1]
        mock_adaptive_test.check_se_criterion.return_value = False
        mock_adaptive_test.check_length_criterion.side_effect = [True]
        sim = Simulation(test=mock_adaptive_test, test_result_output=ResultOutputFormat.CSV)
        sim.simulate(criterion=StoppingCriterion.LENGTH, value=1)
        self.assertEqual(mock_adaptive_test.run_test_once.call_count, 1)

    def test_simulate_with_multiple_criteria(self):
        mock_adaptive_test = get_mock_adaptive_test()
        mock_adaptive_test.item_pool.test_items = [1, 2]
        
        def se_criterion(val):
            return mock_adaptive_test.run_test_once.call_count == 2
        
        def length_criterion(val):
            return False
        mock_adaptive_test.check_se_criterion.side_effect = se_criterion
        mock_adaptive_test.check_length_criterion.side_effect = length_criterion
        sim = Simulation(test=mock_adaptive_test, test_result_output=ResultOutputFormat.CSV)
        sim.simulate(criterion=[StoppingCriterion.SE, StoppingCriterion.LENGTH], value=0.9)
        self.assertEqual(mock_adaptive_test.run_test_once.call_count, 2)

    def test_save_test_results_unsupported_format(self):
        mock_adaptive_test = get_mock_adaptive_test()
        sim = Simulation(test=mock_adaptive_test, test_result_output="UNSUPPORTED") # type: ignore
        with self.assertRaises(KeyError):
            sim.save_test_results()
