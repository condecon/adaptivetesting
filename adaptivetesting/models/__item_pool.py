from .__test_item import TestItem
from typing import List, overload, Tuple


class ItemPool:
    def __init__(self,
                 test_items: List[TestItem],
                 simulated_responses: List[int] | None = None):
        """An item pool has to be created for an adaptive test.
        For that, a list of test items has to be provided. If the package is used
        to simulate adaptive tests, simulated responses have to be supplied as well.
        The responses are matched to the items internally.
        Therefore, both have to be in the same order.

        Args:
            test_items (List[TestItem]): A list of test items. Necessary for any adaptive test.

            simulated_responses (List[int]): A list of simulated responses. Required for CAT simulations.
        """
        self.test_items: List[TestItem] = test_items
        self.simulated_responses: List[int] | None = simulated_responses

    def get_item(self, index: int) -> Tuple[TestItem, int] | TestItem:
        """Returns item and if defined the simulated response.

        Args:
            index (int): Index of the test item in the item pool to return.

        Returns:
            TestItem or (TestItem, Simulated Response)
        """
        selected_item = self.test_items[index]
        if self.simulated_responses is not None:
            simulated_response = self.simulated_responses[index]
            return selected_item, simulated_response
        else:
            return selected_item
    
    @overload # type: ignore
    def get_item(self, item: TestItem) -> Tuple[TestItem, int] | TestItem:
        """Returns item and if defined the simulated response.

        Args:
            item (TestItem): item to return.

        Returns:
            TestItem or (TestItem, Simulated Response)
        """
        index = self.test_items.index(item)
        selected_item = self.test_items[index]
        if self.simulated_responses is not None:
            simulated_response = self.simulated_responses[index]
            return selected_item, simulated_response
        else:
            return selected_item

    def get_item_response(self, item: TestItem) -> int:
        """
        Gets the simulated response to an item if available.
        A `ValueError` will be raised if a simulated response is not available.

        Args:
            item (TestItem): item to get the corresponding response

        Returns:
            (int): response (either `0` or `1`)
        """
        if self.simulated_responses is None:
            raise ValueError("Simulated responses not provided")
        else:
            i, res = self.get_item(item) # type: ignore
            return res

    def delete_item(self, item: TestItem) -> None:
        """Deletes item from item pool.
        If simulated responses are defined, they will be deleted as well.

        Args:
            item (TestItem): The test item to delete.
        """
        # get index
        index = self.test_items.index(item)
        # remove item at index
        self.test_items.pop(index)
        # remove response at index
        if self.simulated_responses is not None:
            self.simulated_responses.pop(index)
