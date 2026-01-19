from .__test_item import BaseItem
from typing import List, Tuple


class BaseItemPool:
    def __init__(self,
                 test_items: List[BaseItem],
                 simulated_responses: List[int] | None = None):
        self.test_items: List[BaseItem] = test_items
        self.simulated_responses: List[int] | None = simulated_responses

    def get_item_by_index(self, index: int) -> Tuple[BaseItem, int] | BaseItem:
        selected_item = self.test_items[index]
        if self.simulated_responses is not None:
            simulated_response = self.simulated_responses[index]
            return selected_item, simulated_response
        else:
            return selected_item

    def get_item_by_item(self, item: BaseItem) -> Tuple[BaseItem, int] | BaseItem:
        index = self.test_items.index(item)
        selected_item = self.test_items[index]
        if self.simulated_responses is not None:
            simulated_response = self.simulated_responses[index]
            return selected_item, simulated_response
        else:
            return selected_item

    def get_item_response(self, item: BaseItem) -> int:
        if self.simulated_responses is None:
            raise ValueError("Simulated responses not provided")
        else:
            i, res = self.get_item_by_item(item) # type: ignore
            return res

    def delete_item(self, item: BaseItem) -> None:
        index = self.test_items.index(item)
        self.test_items.pop(index)
        if self.simulated_responses is not None:
            self.simulated_responses.pop(index)

    @staticmethod
    def load_from_list(*args, **kwargs):
        """
        Abstract static method for loading from list. Should be overridden in subclasses.
        """
        raise NotImplementedError("load_from_list must be implemented in subclass")

    @staticmethod
    def load_from_dict(*args, **kwargs):
        """
        Abstract static method for loading from dict. Should be overridden in subclasses.
        """
        raise NotImplementedError("load_from_dict must be implemented in subclass")

    @staticmethod
    def load_from_dataframe(*args, **kwargs):
        """
        Abstract static method for loading from dataframe. Should be overridden in subclasses.
        """
        raise NotImplementedError("load_from_dataframe must be implemented in subclass")
