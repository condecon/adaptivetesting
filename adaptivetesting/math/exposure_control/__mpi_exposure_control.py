from ..content_balancing.__maximum_priority_index import MaximumPriorityIndex
from .__exposure_control import ExposureControl


class MaximumPriorityIndexExposureControl(MaximumPriorityIndex, ExposureControl):
    """This is a reimplementation of the Maximum Priority Index for Exposure Control.
    For further information see `MaximumPriorityIndex`.
    """
    def __init__(self, adaptive_test, constraints):
        super().__init__(adaptive_test, constraints)

    def select_item(self):
        """Select the next item to administer based on the maximum priority index method.
        Returns:
            TestItem: The selected test item.
        """
        return super().select_item()