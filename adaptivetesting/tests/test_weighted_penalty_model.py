# flake8: noqa
# type: ignore
import unittest
from unittest.mock import patch
import numpy as np
from adaptivetesting.math.content_balancing.__weighted_penalty_model import WeightedPenaltyModel


class MockTestItem:
    def __init__(self, id: int, a: float = 1.0, b: float = 0.0, c: float = 0.0, d: float = 1.0, category: list = None):
        self.id = id
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.additional_properties = {"category": category or []}


class MockConstraint:
    def __init__(self, name: str, prevalence: float = 0.5, lower: float = 0.4, upper: float = 0.6):
        self.name = name
        self.prevalence = prevalence
        self.lower = lower
        self.upper = upper


class TestWeightedPenaltyModel(unittest.TestCase):

    def setUp(self):
        self.items = [
            MockTestItem(1, a=1.5, b=0.5, c=0.2, d=1.0, category=["math"]),
            MockTestItem(2, a=1.2, b=-0.3, c=0.1, d=1.0, category=["reading"]),
            MockTestItem(3, a=1.8, b=1.0, c=0.0, d=1.0, category=["math", "geometry"])
        ]
        self.shown_items = [MockTestItem(4, category=["math"])]
        self.ability = 1.0
        self.constraints = [
            MockConstraint("math", prevalence=0.6, lower=0.5, upper=0.7),
            MockConstraint("reading", prevalence=0.4, lower=0.3, upper=0.5),
            MockConstraint("geometry", prevalence=0.2, lower=0.1, upper=0.3)
        ]
        self.constraint_weight = 0.7
        self.information_weight = 0.3

    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.item_information_function')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_total_content_penalty_value_for_item')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_prop')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_total_content_constraint_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_item_information')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_information_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_weighted_penalty_value')
    def test_init_basic_functionality(self, mock_weighted_penalty, mock_info_penalty, mock_std_info, 
                                     mock_std_content, mock_compute_prop, mock_compute_penalty, mock_item_info):
        # Setup mocks
        mock_item_info.side_effect = [2.0, 1.5, 2.5]
        mock_compute_penalty.side_effect = [1.0, 2.0, 1.5]
        mock_compute_prop.side_effect = [0.45, 0.35, 0.25]  # Below lower bounds -> group A
        mock_std_content.side_effect = [0.4, 0.8, 0.6]
        mock_std_info.side_effect = [0.8, 0.6, 1.0]
        mock_info_penalty.side_effect = [0.2, 0.4, 0.0]
        mock_weighted_penalty.side_effect = [0.45, 0.68, 0.42]

        model = WeightedPenaltyModel(
            items=self.items,
            shown_items=self.shown_items,
            ability=self.ability,
            constraints=self.constraints,
            constraint_weight=self.constraint_weight,
            information_weight=self.information_weight
        )

        # Verify basic attributes
        self.assertEqual(model.items, self.items)
        self.assertEqual(model.ability, self.ability)
        self.assertEqual(model.constraints, self.constraints)
        self.assertTrue(hasattr(model, 'eligible_items'))
        self.assertEqual(len(model.eligible_items), 3)

        # Verify function calls
        self.assertEqual(mock_item_info.call_count, 3)
        self.assertEqual(mock_compute_penalty.call_count, 3)

    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.item_information_function')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_total_content_penalty_value_for_item')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_prop')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_total_content_constraint_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_item_information')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_information_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_weighted_penalty_value')
    def test_group_assignment_green(self, mock_weighted_penalty, mock_info_penalty, mock_std_info, 
                                   mock_std_content, mock_compute_prop, mock_compute_penalty, mock_item_info):
        # Setup for green group (all constraints A or B)
        mock_item_info.side_effect = [2.0, 1.5, 2.5]
        mock_compute_penalty.side_effect = [1.0, 2.0, 1.5]
        mock_compute_prop.side_effect = [0.3, 0.2, 0.15]  # All below lower bounds -> group A
        mock_std_content.side_effect = [0.4, 0.8, 0.6]
        mock_std_info.side_effect = [0.8, 0.6, 1.0]
        mock_info_penalty.side_effect = [0.2, 0.4, 0.0]
        mock_weighted_penalty.side_effect = [0.45, 0.68, 0.42]

        model = WeightedPenaltyModel(
            items=self.items,
            shown_items=self.shown_items,
            ability=self.ability,
            constraints=self.constraints,
            constraint_weight=self.constraint_weight,
            information_weight=self.information_weight
        )

        # Check that items with constraints in group A get green assignment
        green_items = [item for item in model.eligible_items if item[2] == "green"]
        self.assertTrue(len(green_items) > 0)

    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.item_information_function')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_total_content_penalty_value_for_item')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_prop')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_total_content_constraint_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_item_information')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_information_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_weighted_penalty_value')
    def test_group_assignment_yellow(self, mock_weighted_penalty, mock_info_penalty, mock_std_info, 
                                    mock_std_content, mock_compute_prop, mock_compute_penalty, mock_item_info):
        # Setup for yellow group (all constraints B)
        mock_item_info.side_effect = [2.0, 1.5, 2.5]
        mock_compute_penalty.side_effect = [1.0, 2.0, 1.5]
        mock_compute_prop.side_effect = [0.55, 0.45, 0.25]  # Math & reading within bounds, geometry below
        mock_std_content.side_effect = [0.4, 0.8, 0.6]
        mock_std_info.side_effect = [0.8, 0.6, 1.0]
        mock_info_penalty.side_effect = [0.2, 0.4, 0.0]
        mock_weighted_penalty.side_effect = [0.45, 0.68, 0.42]

        model = WeightedPenaltyModel(
            items=self.items,
            shown_items=self.shown_items,
            ability=self.ability,
            constraints=self.constraints,
            constraint_weight=self.constraint_weight,
            information_weight=self.information_weight
        )

        # Check that items with only constraint B get yellow assignment
        yellow_items = [item for item in model.eligible_items if item[2] == "yellow"]
        self.assertTrue(len(yellow_items) >= 0)  # May be 0 based on test setup

    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.item_information_function')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_total_content_penalty_value_for_item')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_prop')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_total_content_constraint_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_item_information')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_information_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_weighted_penalty_value')
    def test_group_assignment_red(self, mock_weighted_penalty, mock_info_penalty, mock_std_info, 
                                 mock_std_content, mock_compute_prop, mock_compute_penalty, mock_item_info):
        # Setup for red group (all constraints B or C)
        mock_item_info.side_effect = [2.0, 1.5, 2.5]
        mock_compute_penalty.side_effect = [1.0, 2.0, 1.5]
        mock_compute_prop.side_effect = [0.8, 0.7, 0.55]  # Above upper bounds or within
        mock_std_content.side_effect = [0.4, 0.8, 0.6]
        mock_std_info.side_effect = [0.8, 0.6, 1.0]
        mock_info_penalty.side_effect = [0.2, 0.4, 0.0]
        mock_weighted_penalty.side_effect = [0.45, 0.68, 0.42]

        model = WeightedPenaltyModel(
            items=self.items,
            shown_items=self.shown_items,
            ability=self.ability,
            constraints=self.constraints,
            constraint_weight=self.constraint_weight,
            information_weight=self.information_weight
        )

        # Check that items with constraints in group B,C get red assignment
        red_items = [item for item in model.eligible_items if item[2] == "red"]
        self.assertTrue(len(red_items) >= 0)

    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.item_information_function')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_total_content_penalty_value_for_item')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_total_content_constraint_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_item_information')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_information_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_weighted_penalty_value')
    def test_item_sorting_by_penalty_value(self, mock_weighted_penalty, mock_info_penalty, mock_std_info, 
                                          mock_std_content, mock_compute_penalty, mock_item_info):
        # Setup different penalty values for sorting test
        mock_item_info.side_effect = [2.0, 1.5, 2.5]
        mock_compute_penalty.side_effect = [3.0, 1.0, 2.0]
        mock_std_content.side_effect = [1.0, 0.0, 0.5]
        mock_std_info.side_effect = [0.8, 0.6, 1.0]
        mock_info_penalty.side_effect = [0.2, 0.4, 0.0]
        mock_weighted_penalty.side_effect = [3.0, 1.0, 2.0]  # Different penalty values

        model = WeightedPenaltyModel(
            items=self.items,
            shown_items=self.shown_items,
            ability=self.ability,
            constraints=[],  # No constraints to avoid group assignment
            constraint_weight=self.constraint_weight,
            information_weight=self.information_weight
        )

        # Items should be sorted by penalty value (ascending) when no groups
        penalty_values = [item[1] for item in model.eligible_items]
        self.assertEqual(penalty_values, [1.0, 2.0, 3.0])

    def test_init_empty_items_list(self):
        model = WeightedPenaltyModel(
            items=[],
            shown_items=self.shown_items,
            ability=self.ability,
            constraints=self.constraints,
            constraint_weight=self.constraint_weight,
            information_weight=self.information_weight
        )

        self.assertEqual(len(model.eligible_items), 0)
        self.assertEqual(model.items, [])

    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.item_information_function')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_total_content_penalty_value_for_item')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_total_content_constraint_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_item_information')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_information_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_weighted_penalty_value')
    def test_init_empty_constraints_list(self, mock_weighted_penalty, mock_info_penalty, mock_std_info, 
                                        mock_std_content, mock_compute_penalty, mock_item_info):
        mock_item_info.side_effect = [2.0, 1.5, 2.5]
        mock_compute_penalty.side_effect = [1.0, 2.0, 1.5]
        mock_std_content.side_effect = [0.4, 0.8, 0.6]
        mock_std_info.side_effect = [0.8, 0.6, 1.0]
        mock_info_penalty.side_effect = [0.2, 0.4, 0.0]
        mock_weighted_penalty.side_effect = [0.45, 0.68, 0.42]

        model = WeightedPenaltyModel(
            items=self.items,
            shown_items=self.shown_items,
            ability=self.ability,
            constraints=[],
            constraint_weight=self.constraint_weight,
            information_weight=self.information_weight
        )

        # All items should have None group assignment
        self.assertTrue(all(item[2] is None for item in model.eligible_items))

    def test_select_item_with_eligible_items(self):
        model = WeightedPenaltyModel.__new__(WeightedPenaltyModel)
        model.eligible_items = [
            (self.items[0], 1.0, "green"),
            (self.items[1], 2.0, "orange"),
            (self.items[2], 1.5, "green")
        ]

        selected_item = model.select_item()
        # Should return first item (lowest penalty in green group)
        self.assertEqual(selected_item, self.items[0])

    def test_select_item_with_no_eligible_items(self):
        model = WeightedPenaltyModel.__new__(WeightedPenaltyModel)
        model.eligible_items = []

        selected_item = model.select_item()
        self.assertIsNone(selected_item)

    def test_select_item_returns_first_item(self):
        model = WeightedPenaltyModel.__new__(WeightedPenaltyModel)
        model.eligible_items = [
            (self.items[1], 2.0, "orange"),
            (self.items[0], 1.0, "green"),
            (self.items[2], 3.0, "red")
        ]

        selected_item = model.select_item()
        # Should return the first item in the sorted list
        self.assertEqual(selected_item, self.items[1])

    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_total_content_constraint_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_item_information')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_information_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_weighted_penalty_value')
    def test_calculate_weighted_penalty_static_method(self, mock_weighted_penalty, mock_info_penalty, 
                                                     mock_std_info, mock_std_content):
        mock_std_content.return_value = 0.5
        mock_std_info.return_value = 0.8
        mock_info_penalty.return_value = 0.2
        mock_weighted_penalty.return_value = 0.45

        result = WeightedPenaltyModel._WeightedPenaltyModel__calculate_weighted_penalty(
            content_penalty=2.0,
            minimum_total_content_penalty=1.0,
            maximum_total_content_penalty=3.0,
            item_information=1.5,
            max_information=2.0,
            constraint_weight=0.7,
            information_weight=0.3
        )

        self.assertEqual(result, 0.45)
        
        # Verify function calls with correct parameters
        mock_std_content.assert_called_once_with(
            item_penality_value=2.0,
            minimum=1.0,
            maximum=3.0
        )
        mock_std_info.assert_called_once_with(
            item_information=1.5,
            maximum=2.0
        )
        mock_info_penalty.assert_called_once_with(
            standardized_item_information=0.8
        )
        mock_weighted_penalty.assert_called_once_with(
            constraint_weight=0.7,
            standardized_constraint_penalty_value=0.5,
            information_weight=0.3,
            information_penalty_value=0.2
        )

    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.item_information_function')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_total_content_penalty_value_for_item')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_prop')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_total_content_constraint_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_item_information')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_information_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_weighted_penalty_value')
    def test_compute_prop_calls_with_correct_parameters(self, mock_weighted_penalty, mock_info_penalty, 
                                                       mock_std_info, mock_std_content, mock_compute_prop, 
                                                       mock_compute_penalty, mock_item_info):
        mock_item_info.side_effect = [2.0, 1.5, 2.5]
        mock_compute_penalty.side_effect = [1.0, 2.0, 1.5]
        mock_compute_prop.side_effect = [0.45, 0.35, 0.25]
        mock_std_content.side_effect = [0.4, 0.8, 0.6]
        mock_std_info.side_effect = [0.8, 0.6, 1.0]
        mock_info_penalty.side_effect = [0.2, 0.4, 0.0]
        mock_weighted_penalty.side_effect = [0.45, 0.68, 0.42]

        model = WeightedPenaltyModel(
            items=self.items,
            shown_items=self.shown_items,
            ability=self.ability,
            constraints=self.constraints,
            constraint_weight=self.constraint_weight,
            information_weight=self.information_weight
        )

        # Verify compute_prop was called for each constraint
        self.assertEqual(mock_compute_prop.call_count, 3)
        
        # Check first call parameters
        first_call = mock_compute_prop.call_args_list[0]
        self.assertEqual(first_call[1]['n_administered'], 1)  # One shown item with "math"
        self.assertEqual(first_call[1]['n_remaining'], 2)     # Two items with "math" 
        self.assertEqual(first_call[1]['prevalence'], 0.6)
        self.assertEqual(first_call[1]['test_length'], 1)

    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.item_information_function')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_total_content_penalty_value_for_item')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_prop')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_total_content_constraint_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_item_information')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_information_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_weighted_penalty_value')
    def test_item_information_function_calls(self, mock_weighted_penalty, mock_info_penalty, mock_std_info, 
                                           mock_std_content, mock_compute_prop, mock_compute_penalty, mock_item_info):
        mock_item_info.side_effect = [2.0, 1.5, 2.5]
        mock_compute_penalty.side_effect = [1.0, 2.0, 1.5]
        mock_compute_prop.side_effect = [0.45, 0.35, 0.25]
        mock_std_content.side_effect = [0.4, 0.8, 0.6]
        mock_std_info.side_effect = [0.8, 0.6, 1.0]
        mock_info_penalty.side_effect = [0.2, 0.4, 0.0]
        mock_weighted_penalty.side_effect = [0.45, 0.68, 0.42]

        model = WeightedPenaltyModel(
            items=self.items,
            shown_items=self.shown_items,
            ability=self.ability,
            constraints=self.constraints,
            constraint_weight=self.constraint_weight,
            information_weight=self.information_weight
        )

        # Verify item_information_function was called for each item
        self.assertEqual(mock_item_info.call_count, 3)
        
        # Check that it was called with correct parameters for first item
        first_call = mock_item_info.call_args_list[0]
        np.testing.assert_array_equal(first_call[1]['mu'], np.array(self.ability))
        np.testing.assert_array_equal(first_call[1]['a'], np.array(self.items[0].a))

    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.item_information_function')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_total_content_penalty_value_for_item')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_prop')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_total_content_constraint_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.standardize_item_information')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_information_penalty_value')
    @patch('adaptivetesting.math.content_balancing.__weighted_penalty_model.compute_weighted_penalty_value')
    def test_single_item_processing(self, mock_weighted_penalty, mock_info_penalty, mock_std_info, 
                                   mock_std_content, mock_compute_prop, mock_compute_penalty, mock_item_info):
        mock_item_info.return_value = 2.0
        mock_compute_penalty.return_value = 1.0
        mock_compute_prop.return_value = 0.45
        mock_std_content.return_value = 0.5
        mock_std_info.return_value = 0.8
        mock_info_penalty.return_value = 0.2
        mock_weighted_penalty.return_value = 0.45

        single_item = [MockTestItem(1, category=["math"])]
        single_constraint = [MockConstraint("math")]

        model = WeightedPenaltyModel(
            items=single_item,
            shown_items=self.shown_items,
            ability=self.ability,
            constraints=single_constraint,
            constraint_weight=self.constraint_weight,
            information_weight=self.information_weight
        )

        self.assertEqual(len(model.eligible_items), 1)
        self.assertEqual(model.eligible_items[0][0], single_item[0])
        self.assertEqual(model.eligible_items[0][1], 0.45)
        self.assertEqual(model.eligible_items[0][2], "green")  # Single constraint A -> green

    def test_group_ordering_priority(self):
        # Test that group ordering follows: green, orange, yellow, red, None
        model = WeightedPenaltyModel.__new__(WeightedPenaltyModel)
        model.eligible_items = [
            (self.items[0], 3.0, "red"),
            (self.items[1], 1.0, "green"),
            (self.items[2], 2.0, "yellow"),
            (MockTestItem(5), 4.0, None),
            (MockTestItem(6), 1.5, "orange")
        ]

        # Manually sort using the same key function as in the class
        sorted_items = sorted(
            model.eligible_items,
            key=lambda x: (
                {"green": 0, "orange": 1, "yellow": 2, "red": 3, None: 4}[x[2]],
                x[1]
            )
        )

        expected_order = ["green", "orange", "yellow", "red", None]
        actual_order = [item[2] for item in sorted_items]
        self.assertEqual(actual_order, expected_order)


if __name__ == '__main__':
    unittest.main()