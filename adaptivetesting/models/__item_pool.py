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

    def get_item_by_index(self, index: int) -> Tuple[TestItem, int] | TestItem:
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
    
    def get_item_by_item(self, item: TestItem) -> Tuple[TestItem, int] | TestItem:
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
            i, res = self.get_item_by_item(item) # type: ignore
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

    @staticmethod
    def load_from_list(
        b: List[float],
        a: List[float] | None = None,
        c: List[float] | None = None,
        d: List[float] | None = None,
        ) -> "ItemPool":
        """Creates test items from a list of floats.

        Args:
            a (List[float]): discrimination parameter
            b (List[float]): difficulty parameter
            c (List[float]): guessing parameter
            d (jnp.ndarray): slipping parameter

        Returns:
            List[TestItem]: item pool
        """
        items: List[TestItem] = []

        for difficulty in b:
            item = TestItem()
            item.b = difficulty
            items.append(item)

        # check if a, b, c, d are the same length
        if a is not None:
            if len(a) != len(b):
                raise ValueError("Length of a and b has to be the same.")
            for i, discrimination in enumerate(a):
                items[i].a = discrimination
        
        if c is not None:
            if len(c) != len(b):
                raise ValueError("Length of c and b has to be the same.")
            for i, guessing in enumerate(c):
                items[i].c = guessing
        
        if d is not None:
            if len(d) != len(b):
                raise ValueError("Length of d and b has to be the same.")
            for i, slipping in enumerate(d):
                items[i].d = slipping

        return items

    @staticmethod
    def load_from_dict(source: dict[str, List[float]]) -> "ItemPool":
        """Creates test items from a dictionary.
        The dictionary has to have the following keys:
            
            - a
            - b
            - c
            - d
        each containing a list of float.

        Args:
            source (dict[str, List[float]]): item pool dictionary

        Returns:
            List[TestItem]: item pool
        """
        a = source.get("a")
        b = source.get("b")
        c = source.get("c")
        d = source.get("d")

        # check none
        if a is None:
            raise ValueError("a cannot be None")
        
        if b is None:
            raise ValueError("b cannot be None")
        
        if c is None:
            raise ValueError("c cannot be None")
        
        if d is None:
            raise ValueError("d cannot be None")

        # check if a, b, c, and d have the same length
        if not (len(a) == len(b) == len(c) == len(d)):
            raise ValueError("All lists in the source dictionary must have the same length")

        n_items = len(b)
        items: List[TestItem] = []
        for i in range(n_items):
            item = TestItem()
            item.a = a[i]
            item.b = b[i]
            item.c = c[i]
            item.d = d[i]

            items.append(item)

        return items        