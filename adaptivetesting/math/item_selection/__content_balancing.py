from ...models.__test_item import TestItem
from ...models.__item_selection_exception import ItemSelectionException
from ...math.estimators.__test_information import item_information_function
import numpy as np
import abc


class ContentBalancing(abc.ABC):
    def __init__(self):
        super().__init__()


# WORK IN PROGRESS    
class MaximumPriorityIndexMethod(ContentBalancing):
    def __init__(self,
                 available_items: list[TestItem],
                 shown_items: list[TestItem],
                 fisher_information: np.ndarray,
                 groups: list[str],
                 quota: list[float]
                 ):
        self.available_items = available_items
        self.fisher_information = fisher_information
        self.shown_items = shown_items
        self.groups = groups
        self.quota = quota

        # sort items by id
        self.available_items.sort(key=lambda item: item.id)
        
        super().__init__()

