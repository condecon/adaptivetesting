from ..content_balancing.__maximum_priority_index import MaximumPriorityIndex
from .__exposure_control import ExposureControl
from ...models.__test_item import TestItem
from ...models.__misc import ResultOutputFormat
from ..content_balancing.__functions import compute_priority_index
import numpy as np
from ...data.__read_prev_items_exp_cont import read_prev_items
from typing import Literal


class MaximumPriorityIndexExposureControl(MaximumPriorityIndex, ExposureControl):
    """This is a reimplementation of the Maximum Priority Index for Exposure Control.
    For further information see `MaximumPriorityIndex`.
    """
    def __init__(self, adaptive_test, constraints, participant_ids: list[str], format: ResultOutputFormat):
        super().__init__(adaptive_test, constraints)
        self.participant_ids = participant_ids
        self.format = format

    def select_item(self, **kwargs) -> TestItem | None:
        """Select the next item to administer based on the maximum priority index method.
        Returns:
            TestItem: The selected test item.
        """
        # compute priority index for every item
        available_items = self.adaptive_test.item_pool.test_items
        # skip seletion if item pool is empty
        if len(available_items) == 0:
            return None

        # load items that have been shown to other users
        format: Literal["CSV", "PICKLE"]
        if self.format is ResultOutputFormat.CSV:
            format = "CSV"
        if self.format is ResultOutputFormat.PICKLE:
            format = "PICKLE"
        shown_items = read_prev_items(
            test_id=self.adaptive_test.simulation_id,
            participant_ids=self.participant_ids,
            format=format
        )
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
