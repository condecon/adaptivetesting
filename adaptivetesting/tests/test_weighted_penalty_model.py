import unittest
import pandas as pd
import adaptivetesting as adt
import copy
from typing import Literal

class MockItem(adt.TestItem):
    def __init__(self, category: list[str]):
        super().__init__()
        self.additional_properties["category"] = category


class TestWeightedPenaltyModel(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

        # load test item pool
        data_frame = pd.read_json("adaptivetesting/tests/example_item_pool.json")
        # convert list[dict] into item pool
        self.item_pool = adt.ItemPool.load_from_dataframe(data_frame)

        # create two example items fitting a rasch model
        self.example_item1 = adt.TestItem()
        self.example_item1.id = 1
        self.example_item1.a = 1; self.example_item1.b = 0.5; self.example_item1.c = 0; self.example_item1.d = 1
        self.example_item1.additional_properties["category"] = ["math"]

        self.example_item2 = adt.TestItem()
        self.example_item2.id = 2
        self.example_item2.a = 1; self.example_item2.b = 0.5; self.example_item2.c = 0; self.example_item2.d = 1
        self.example_item2.additional_properties["category"] = ["english"]

    def test_content_penalty_calculation(self):
        """compute_total_content_penalty_value_for_item"""
        # create target item
        item = copy.deepcopy(self.example_item1)
        item.additional_properties["category"] = ["math", "science"]

        # create shown items for math and science
        shown_items = [
            MockItem(["math"]),
            MockItem(["math"]),
            MockItem(["science"])
        ]

        # setup constraints
        constraints = [
            adt.Constraint(
                name="math",
                prevalence=0.75,
                lower=0,
                upper=1,
                weight=1
            ),
            adt.Constraint(
                name="science",
                prevalence=0.25,
                lower=0,
                upper=1,
                weight=1
            )
        ]

        total_content_penalty_value = adt.compute_total_content_penalty_value_for_item(
            item,
            shown_items=shown_items,
            available_items=[item],
            constraints=constraints
        )

        manual_result = 0.4166 - 0.083
        
        self.assertAlmostEqual(total_content_penalty_value,
                               manual_result, places=2)

    def test_calcualte_weighted_content_penalty(self):
        """calculate_weighted_penalty_value"""
        item_information = 0.5
        max_information = 1
        constraint_weight = 1
        information_weight = 1
        total_content_penalty = 0.5
        maximum_total_content_penalty = 0.8
        minimum_total_content_penalty = 0.2

        # standardize total content constraint penalty value
        standardized_total_content_penalty_value = adt.standardize_total_content_constraint_penalty_value(
            item_penalty_value=total_content_penalty,
            minimum=minimum_total_content_penalty,
            maximum=maximum_total_content_penalty
        )

        self.assertAlmostEqual(standardized_total_content_penalty_value, 0.5, places=2)

        # standardize item information
        standardized_item_information = adt.standardize_item_information(
            item_information=item_information,
            maximum=max_information
        )
        self.assertAlmostEqual(standardized_item_information, 0.5, places=2)

        # calculate information penalty value
        information_penalty_value = adt.compute_information_penalty_value(
            standardized_item_information
        )

        self.assertAlmostEqual(information_penalty_value, -0.25, places=2)

        # compute weighted penalty vlaue
        weighted_penalty_value = adt.compute_weighted_penalty_value(
            constraint_weight=constraint_weight,
            standardized_constraint_penalty_value=standardized_total_content_penalty_value,
            information_weight=information_weight,
            information_penalty_value=information_penalty_value
        )

        self.assertAlmostEqual(weighted_penalty_value, 0.25, places=2)

    def test_constraint_group_assignment(self):
        """get_constraint_group_assignments"""

        # create shown items for math and science
        shown_items = [
            MockItem(["math"]),
            MockItem(["math"]),
            MockItem(["science"])
        ]

        # setup constraints
        constraints = [
            adt.Constraint(
                name="math",
                prevalence=0.75,
                lower=0,
                upper=1,
                weight=1
            ),
            adt.Constraint(
                name="science",
                prevalence=0.25,
                lower=0.9,
                upper=1,
                weight=1
            )
        ]
        
        assignments = []
        for constraint in constraints:
            # calculate proportion
            prop = adt.compute_prop(
                n_administered=1,
                n_remaining=1,
                prevalence=constraint.prevalence,
                test_length=2
            )

            # assign color group per proportion
            _, assignment = adt.WeightedPenaltyModel.assign_color_group_per_proportion(
                constraint,
                prop
            )
            assignments.append(assignment)

        self.assertListEqual(assignments, ["B", "A"])

    
    def test_candidate_group_assignment(self):
        """form_list_of_candidate_items"""
        # create item
        item = MockItem("None")
        weighted_penalty_value = float("NaN")
        # test green
        associated_constraints: list[tuple[adt.Constraint, Literal['A', 'B', 'C']]] = [
            (adt.Constraint(None, None, None), "A"),
            (adt.Constraint(None, None, None), "B")
        ]
        _, _, assigned_group = adt.WeightedPenaltyModel.assign_items_to_item_group(
            item, associated_constraints,
            weighted_penalty_value
        )
        self.assertEqual(assigned_group, "green")

        # test organge
        associated_constraints: list[tuple[adt.Constraint, Literal['A', 'B', 'C']]] = [
            (adt.Constraint(None, None, None), "A"),
            (adt.Constraint(None, None, None), "C")
        ]
        _, _, assigned_group = adt.WeightedPenaltyModel.assign_items_to_item_group(
            item, associated_constraints,
            weighted_penalty_value
        )
        self.assertEqual(assigned_group, "orange")

        # test yellow
        associated_constraints: list[tuple[adt.Constraint, Literal['A', 'B', 'C']]] = [
            (adt.Constraint(None, None, None), "B"),
            (adt.Constraint(None, None, None), "B")
        ]
        _, _, assigned_group = adt.WeightedPenaltyModel.assign_items_to_item_group(
            item, associated_constraints,
            weighted_penalty_value
        )
        self.assertEqual(assigned_group, "yellow")

        # test red
        associated_constraints: list[tuple[adt.Constraint, Literal['A', 'B', 'C']]] = [
            (adt.Constraint(None, None, None), "B"),
            (adt.Constraint(None, None, None), "C")
        ]
        _, _, assigned_group = adt.WeightedPenaltyModel.assign_items_to_item_group(
            item, associated_constraints,
            weighted_penalty_value
        )
        self.assertEqual(assigned_group, "red")
