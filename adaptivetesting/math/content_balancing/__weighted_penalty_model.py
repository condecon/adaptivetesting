from typing import Literal
import numpy as np
from ..estimators.__test_information import item_information_function
from ...models.__test_item import TestItem
from .__functions import (
    compute_prop,
    compute_total_content_penalty_value_for_item,
    standardize_total_content_constraint_penalty_value,
    standardize_item_information,
    compute_information_penalty_value,
    compute_weighted_penalty_value
)
from .__constraint import Constraint


CONSTRAINT_GROUP = Literal["A", "B", "C"]
ITEM_GROUP = Literal["green", "orange", "yellow", "red", None]


class WeightedPenaltyModel:
    def __init__(self,
                 items: list[TestItem],
                 shown_items: list[TestItem],
                 ability: float,
                 constraints: list[Constraint],
                 constraint_weight: float,
                 information_weight: float
                 ):
        self.items = items
        self.ability = ability
        self.constraints = constraints
        self.eligible_items: list[tuple[TestItem, float, ITEM_GROUP]] = []
        self.shown_items = shown_items
        self.constraint_weight = constraint_weight
        self.information_weight = information_weight

    def select_item(self) -> TestItem | None:
        """Select the next item to administer based on the weighted penalty model.

        Returns:
            TestItem | None: The selected TestItem or None if no eligible items are available.
        """
        self.prepare_item_pool()
        if len(self.eligible_items) > 0:
            return self.eligible_items[0][0]
        else:
            return None
    
    def prepare_item_pool(self):
        """Prepares item pool for the item selection
        and calls are functions required to perform the necessary calculations"""
        # calculate item information for every item
        item_information_list = self.calculate_information()

        max_item = max(item_information_list)

        content_penalties = self.calculate_content_penalties()

        max_content_penalty = max(content_penalties)
        min_content_penalty = min(content_penalties)

        self.calcualte_weighted_penalty_for_all_items(
            item_information_list=item_information_list,
            max_item=max_item,
            content_penalties=content_penalties,
            max_content_penalty=max_content_penalty,
            min_content_penalty=min_content_penalty
        )

        group_assignment: list[tuple[Constraint, CONSTRAINT_GROUP]] = self.get_constraint_group_assignments()

        # form a list of candidate items
        self.form_list_of_candidate_items(group_assignment)

        # order items
        self.order_candidate_items()

    def calculate_information(self) -> list[float]:
        information_list = [
            float(item_information_function(
                mu=np.array(self.ability),
                a=np.array(item.a),
                b=np.array(item.b),
                c=np.array(item.c),
                d=np.array(item.d)
            ))
            for item in self.items
        ]
        return information_list

    def calculate_content_penalties(self) -> list[float]:
        content_penalties = [
            compute_total_content_penalty_value_for_item(
                item=item,
                shown_items=self.shown_items,
                available_items=self.items,
                constraints=self.constraints
            )
            for item in self.items
        ]
        return content_penalties

    def calcualte_weighted_penalty_for_all_items(self,
                                                 item_information_list: list[float],
                                                 max_item: float,
                                                 content_penalties: list[float],
                                                 max_content_penalty: float,
                                                 min_content_penalty: float):
        for i, item in enumerate(self.items):
            weighted_penalty_value = self.calculate_weighted_penalty_value(
                item_information=item_information_list[i],
                max_information=max_item,
                constraint_weight=self.constraint_weight,
                information_weight=self.information_weight,
                content_penalty=content_penalties[i],
                maximum_total_content_penalty=max_content_penalty,
                minimum_total_content_penalty=min_content_penalty,
            )

            self.eligible_items.append((item, weighted_penalty_value, None))

    def get_constraint_group_assignments(self) -> list[tuple[Constraint, CONSTRAINT_GROUP]]:
        group_assignment: list[tuple[Constraint, CONSTRAINT_GROUP]] = []
        for constraint in self.constraints:
            # calculate proportion of the constraint
            n_administered: int = len(
                [item for item in self.shown_items if constraint.name in item.additional_properties["category"]]
            )
            n_remaining: int = len(
                [item for item in self.items if constraint.name in item.additional_properties["category"]]
            )
            test_length: int = len(self.shown_items)
            prop = compute_prop(
                n_administered=n_administered,
                n_remaining=n_remaining,
                prevalence=constraint.prevalence,
                test_length=test_length,
            )
            # assign color group per proportion
            if constraint.lower is not None and constraint.upper is not None:
                if prop <= constraint.lower:
                    group_assignment.append((constraint, "A"))
                if constraint.lower <= prop <= constraint.upper:
                    group_assignment.append((constraint, "B"))
                if constraint.upper <= prop:
                    group_assignment.append((constraint, "C"))
            else:
                raise ValueError("constraint.lower and constraint upper may not be None.")

        return group_assignment

    def form_list_of_candidate_items(self,
                                     group_assignment: list[tuple[Constraint, CONSTRAINT_GROUP]]) -> None:
        for i, item_entry in enumerate(self.eligible_items):
            item, weighted_penalty_value, _ = item_entry
            # find associated constraint
            associated_constraints = [constraint_assignment
                                      for constraint_assignment in group_assignment
                                      if constraint_assignment[0].name in item.additional_properties["category"]
                                      ]

            # if all associated constraints A or B -> green group
            if all(group in ["A", "B"] for _, group in associated_constraints):
                self.eligible_items[i] = (item, weighted_penalty_value, "green")
            # if all A, B, C, or A, C -> orange
            if all(group in ["A", "B", "C"] or group in ["A", "C"] for _, group in associated_constraints):
                self.eligible_items[i] = (item, weighted_penalty_value, "orange")
            # if all B -> yellow
            if all(group in ["B"] for _, group in associated_constraints):
                self.eligible_items[i] = (item, weighted_penalty_value, "yellow")
            # if all B, C -> red
            if all(group in ["B", "C"] for _, group in associated_constraints):
                self.eligible_items[i] = (item, weighted_penalty_value, "red")
            else:
                self.eligible_items[i] = (item, weighted_penalty_value, None)

    def order_candidate_items(self):
        # between group ordering: green, orange, yellow, red
        # within group ordering: ascending order of weighted penalty value
        self.eligible_items = sorted(
            self.eligible_items,
            key=lambda x: (
                {"green": 0, "orange": 1, "yellow": 2, "red": 3, None: 4}[x[2]],
                x[1]
            )
        )

    @staticmethod
    def calculate_weighted_penalty_value(content_penalty: float,
                                         minimum_total_content_penalty: float,
                                         maximum_total_content_penalty: float,
                                         item_information: float,
                                         max_information: float,
                                         constraint_weight: float,
                                         information_weight: float
                                         ) -> float:
        # reference content penalty
        total_content_penalty_value = content_penalty

        # standardize total content constraint penalty value
        standardized_total_content_penalty_value = standardize_total_content_constraint_penalty_value(
            item_penality_value=total_content_penalty_value,
            minimum=minimum_total_content_penalty,
            maximum=maximum_total_content_penalty
        )

        # calculate standardized item information
        standardized_item_information = standardize_item_information(
            item_information=item_information,
            maximum=max_information
        )

        # calculate information penalty value
        information_penalty_value = compute_information_penalty_value(
            standardized_item_information=standardized_item_information
        )

        # compute weighted penality value
        weighted_penalty_value = compute_weighted_penalty_value(
            constraint_weight=constraint_weight,
            standardized_constraint_penalty_value=standardized_total_content_penalty_value,
            information_weight=information_weight,
            information_penalty_value=information_penalty_value,
        )
        return weighted_penalty_value
