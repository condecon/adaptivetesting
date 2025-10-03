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

        # calculate weighted penality value for each eligible item in the pool
        eligible_items: list[tuple[TestItem, float, ITEM_GROUP]] = []
        # calculate item information for every item
        item_information_list = [
            float(item_information_function(
                mu=np.array(ability),
                a=np.array(item.a),
                b=np.array(item.b),
                c=np.array(item.c),
                d=np.array(item.d)
            ))
            for item in self.items
        ]

        max_item = max(item_information_list)

        content_penalties = [
            compute_total_content_penalty_value_for_item(
                item=item,
                shown_items=shown_items,
                available_items=items,
                constraints=constraints
            )
            for item in items
        ]

        max_content_penalties = max(content_penalties)
        min_content_penalties = min(content_penalties)

        for i, item in enumerate(self.items):
            weighted_penalty_value = self.__calculate_weighted_penalty(
                item_information=item_information_list[i],
                max_information=max_item,
                constraint_weight=constraint_weight,
                information_weight=information_weight,
                content_penalty=content_penalties[i],
                maximum_total_content_penalty=max_content_penalties,
                minimum_total_content_penalty=min_content_penalties,
            )

            eligible_items.append((item, weighted_penalty_value, None))

        group_assignment: list[tuple[Constraint, CONSTRAINT_GROUP]] = []
        # assign each constraint to a color group
        for constraint in constraints:
            # calculate proportion of the constraint
            n_administered: int = len(
                [item for item in shown_items if constraint.name in item.additional_properties["category"]]
            )
            n_remaining: int = len(
                [item for item in self.items if constraint.name in item.additional_properties["category"]]
            )
            test_length: int = len(shown_items)
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

        # form a list of candidate items
        for i, item_entry in enumerate(eligible_items):
            item, weighted_penalty_value, _ = item_entry
            # find associated constraint
            associated_constraints = [constraint_assignment
                                      for constraint_assignment in group_assignment
                                      if constraint_assignment[0].name in item.additional_properties["category"]
                                      ]

            # if all associated constraints A or B -> green group
            if all(group in ["A", "B"] for _, group in associated_constraints):
                eligible_items[i] = (item, weighted_penalty_value, "green")
            # if all A, B, C, or A, C -> orange
            if all(group in ["A", "B", "C"] or group in ["A", "C"] for _, group in associated_constraints):
                eligible_items[i] = (item, weighted_penalty_value, "orange")
            # if all B -> yellow
            if all(group in ["B"] for _, group in associated_constraints):
                eligible_items[i] = (item, weighted_penalty_value, "yellow")
            # if all B, C -> red
            if all(group in ["B", "C"] for _, group in associated_constraints):
                eligible_items[i] = (item, weighted_penalty_value, "red")
            else:
                eligible_items[i] = (item, weighted_penalty_value, None)

        # order items
        # between group ordering: green, orange, yellow, red
        # within group ordering: ascending order of weighted penalty value
        self.eligible_items = sorted(
            eligible_items,
            key=lambda x: (
                {"green": 0, "orange": 1, "yellow": 2, "red": 3, None: 4}[x[2]],
                x[1]
            )
        )

    def select_item(self) -> TestItem | None:
        """Select the next item to administer based on the weighted penalty model.

        Returns:
            TestItem | None: The selected TestItem or None if no eligible items are available.
        """
        if len(self.eligible_items) > 0:
            return self.eligible_items[0][0]
        else:
            return None

    @staticmethod
    def __calculate_weighted_penalty(content_penalty: float,
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
