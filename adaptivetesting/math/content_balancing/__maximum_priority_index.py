from .__content_balancing import ContentBalancing
from ...models.__test_item import TestItem
from ...models.__adaptive_test import AdaptiveTest
from .__constraint import Constraint
from .__functions import compute_priority_index
import numpy as np


class MaximumPriorityIndex(ContentBalancing):
    """This content balancing method follows Cheng & Chang (2009).
    A weight it applied to the item information considering the
    current state of constraint fulfillment.

    References
    -----------
    Cheng, Y., & Chang, H. (2009). The maximum priority index method for severely constrained item selection
    in computerized adaptive testing.
    British Journal of Mathematical and Statistical Psychology, 62(2), 369–383.
    https://doi.org/10.1348/000711008X304376

    """
    def __init__(self, adaptive_test: AdaptiveTest, constraints: list[Constraint]):
        """This content balancing method follows Cheng & Chang (2009).
            A weight it applied to the item information considering the
            current state of constraint fulfillment.

        Args:
            adaptive_test (AdaptiveTest): instance of the adaptive test
            constraints (list[Constraint]): constraints that are applied to the item selection
        """
        super().__init__(adaptive_test, constraints)
        self.adaptive_test = adaptive_test
        self.constraints = constraints

    def select_item(self) -> TestItem |None:
        """Select the next item to administer based on the maximum priority index method.
        Returns:
            TestItem: The selected test item.
        """
        # compute priority index for every item
        available_items = self.adaptive_test.item_pool.test_items
        shown_items = self.adaptive_test.answered_items
        priority_indices: list[float] = []
        
        for item in available_items:
            # get associated constraints
            associated_constraints = [
                constraint
                for constraint in self.constraints
                if constraint.name in item.additional_properties["category"]
            ]

            group_weights: dict[str, float] = {}
            required_items: dict[str, float] = {}
            shown_items_per_constraint: dict[str, float] = {}
            
            for constraint in associated_constraints:
                group_weights[constraint.name] = constraint.weight
                required_items[constraint.name] = constraint.prevalence
                n_shown_items = len([
                    shown_item
                    for shown_item in shown_items
                    if constraint.name in shown_item.additional_properties["category"]
                ])
                shown_items_per_constraint[constraint.name] = float(n_shown_items)

            # calculate priority index
            pix = compute_priority_index(
                item=item,
                group_weights=group_weights,
                required_items=required_items,
                shown_items=shown_items_per_constraint,
                current_ability=self.adaptive_test.ability_level
            )

            priority_indices.append(pix)

        # select the item with the highest priority index
        max_p_i = np.argmax(priority_indices)
        selected_item = available_items[max_p_i]

        return selected_item
