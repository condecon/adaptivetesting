from .__test_item import TestItem
from typing import List, Tuple
from pandas import DataFrame


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

            simulated_responses (List[int]): A list of simulated responses.
            Required for CAT simulations.
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

# STATIC LOAD METHODS
    @staticmethod
    def load_from_list(
            b: List[float],
            a: List[float] | None = None,
            c: List[float] | None = None,
            d: List[float] | None = None,
            simulated_responses: List[int] | None = None) -> "ItemPool":
        """
        Creates test items from a list of floats.

        Args:
            a (List[float]): discrimination parameter
            
            b (List[float]): difficulty parameter
            
            c (List[float]): guessing parameter
            
            d (List[float]): slipping parameter
            
            simulated_responses (List[int]): simulated responses

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

        item_pool = ItemPool(items)
        item_pool.simulated_responses = simulated_responses

        return item_pool

    @staticmethod
    def load_from_dict(source: dict[str, List[float]],
                       simulated_responses: List[int] | None = None) -> "ItemPool":
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

        item_pool = ItemPool(items, simulated_responses)
        
        return item_pool
    
    @staticmethod
    def load_from_dataframe(source: DataFrame) -> "ItemPool":
        """Creates item pool from a pandas DataFrame.
        Required columns are: `a`, `b`, `c`, `d`.
        Each column has to contain float values.
        A `simulated_responses` (int values) column can be added to
        the DataFrame to provide simulated responses.
        

        Args:
            source (DataFrame): _description_

        Returns:
            ItemPool: _description_
        """

        # check if columns are present
        if "a" not in source.columns:
            raise ValueError("Column 'a' not found.")
        
        if "b" not in source.columns:
            raise ValueError("Column 'b' not found.")
        
        if "c" not in source.columns:
            raise ValueError("Column 'c' not found.")
        
        if "d" not in source.columns:
            raise ValueError("Column 'd' not found.")
        
        # get values
        a: List[float] = source["a"].values.tolist() # type: ignore
        b: List[float] = source["b"].values.tolist() # type: ignore
        c: List[float] = source["c"].values.tolist() # type: ignore
        d: List[float] = source["d"].values.tolist() # type: ignore

        # create item pool
        item_pool = ItemPool.load_from_list(a=a, b=b, c=c, d=d)
    
        # check if simulated responses are present
        if "simulated_responses" in source.columns:
            simulated_responses: List[int] = source["simulated_responses"].values.tolist() # type: ignore
            item_pool.simulated_responses = simulated_responses
        
        return item_pool
