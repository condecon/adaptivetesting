from .__test_item import TestItem
from typing import List, Tuple, cast
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
            (int): response (either `0` or `1` for dichotmous items or `k` for polytomous items)
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
            b: List[float] | list[list[float]],
            a: List[float] | None = None,
            c: List[float] | None = None,
            d: List[float] | None = None,
            simulated_responses: List[int] | None = None,
            ids: List[int] | None = None,
            content_categories: list[list[str]] | None = None) -> "ItemPool":
        """
        Creates test items from a list of floats.

        Args:
            a (List[float]): discrimination parameter
            b (List[float] | list[list[float]]): For dichotomous models, this is the difficulty parameter.
                For polytomous items, this is the list of threshold parameters.
            c (List[float]): guessing parameter. Ignored for polytomous items.
            d (List[float]): slipping parameter. Ignored for polytomous items.
            simulated_responses (List[int]): simulated responses
            ids (List[int]): item IDs
            content_categories (list[list[str]], optional): List of categories for each item.
                This list is used for content balancing.

        Returns:
            List[TestItem]: item pool

        """
        items: List[TestItem] = []

        for b_i in b:
            item = TestItem()
            item.b = b_i
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

        if ids is not None:
            if len(ids) != len(b):
                raise ValueError("Length of ids and b has to be the same.")
            for i, id_ in enumerate(ids):
                items[i].id = id_

        if content_categories is not None:
            if len(content_categories) != len(b):
                raise ValueError("Length of content_categories and b has to be the same.")
            for i, groups in enumerate(content_categories):
                items[i].additional_properties["category"] = groups

        item_pool = ItemPool(items)
        item_pool.simulated_responses = simulated_responses

        return item_pool

    @staticmethod
    def load_from_dict(source: dict[str, list[float]] | dict[str, list],
                       simulated_responses: List[int] | None = None,
                       ids: List[int] | None = None,
                       content_categories: list[list[str]] | None = None) -> "ItemPool":
        """Creates test items from a dictionary.
        The dictionary has to have the following keys:

            - a
            - b (list of float, for polytomous models list[list[float]] as threshold list)
            - c (ignored for polytomous items)
            - d (ignored for polytomous items)
        each containing a list of float.

        Args:
            source (dict[str, List[float] | list[float]]): item pool dictionary
            simulated_responses (List[int]): simulated responses
            ids (List[int], optional): item IDs. Default `None`.
            content_categories (list[list[str]], optional): List of categories for each item.
                This list is used for content balancing.

        Returns:
            List[TestItem]: item pool
        """
        a = cast(list[float], source.get("a"))
        b = cast(list[list[float]] | list[float], source.get("b"))
        c = cast(list[float] | None, source.get("c"))
        d = cast(list[float] | None, source.get("d"))

        # check none
        if a is None:
            raise ValueError("a cannot be None")

        if b is None:
            raise ValueError("b cannot be None")
        
        if not all([isinstance(b_i, list) for b_i in b]):
            # if b is not a list of thresholds check of c and d
            if c is None:
                raise ValueError("c cannot be None")

            if d is None:
                raise ValueError("d cannot be None")
            # check if a, b, c, and d have the same length
            if not (len(a) == len(b) == len(c) == len(d)):
                raise ValueError("a, b, c, and d must have the same length.")
        else:
            if not (len(a) == len(b)):
                raise ValueError("a and b must have the same length.")
        
        if ids is not None:
            if len(ids) != len(b):
                raise ValueError("Length of ids and b has to be the same.")

        if content_categories is not None:
            if len(content_categories) != len(b):
                raise ValueError("Length of content_categories and b has to be the same.")

        n_items = len(b)
        items: List[TestItem] = []
        for i in range(n_items):
            item = TestItem()
            item.a = a[i]
            item.b = b[i]
            
            if c is not None:
                item.c = c[i]
            if d is not None:
                item.d = d[i]

            if ids is not None:
                item.id = ids[i]
            
            if "id" in source.keys():
                item.id = cast(int, source["id"][i])

            if content_categories is not None:
                item.additional_properties["category"] = content_categories[i]

            items.append(item)

        item_pool = ItemPool(items, simulated_responses)

        return item_pool

    @staticmethod
    def load_from_dataframe(source: DataFrame) -> "ItemPool":
        """Creates item pool from a pandas DataFrame.
        Required columns are: `a`, `b`.
        `c`, `d` are optional (ignored for polytomous items).
        Each column has to contain float values.
        A `simulated_responses` (int values) column can be added to
        the DataFrame to provide simulated responses.

        Args:
            source (DataFrame): source data frame

        Returns:
            ItemPool: parsed item pool
        """

        # check if columns are present
        if "a" not in source.columns:
            raise ValueError("Column 'a' not found.")

        if "b" not in source.columns:
            raise ValueError("Column 'b' not found.")

        # get values
        a: List[float] = source["a"].values.tolist() # type: ignore
        b: List[float] | list[list[float]] = source["b"].values.tolist() # type: ignore
        
        c: list[float] | None
        if "c" in source.columns:
            c: List[float] = source["c"].values.tolist() # type: ignore
        else:
            c = None
        
        d: list[float] | None
        if "d" in source.columns:
            d: List[float] = source["d"].values.tolist() # type: ignore
        else:
            d = None

        if "ids" in source.columns:
            ids: List[int] | None = source["ids"].values.tolist() # type: ignore
        else:
            ids = None

        if "content_categories" in source.columns:
            groups: list[list[str]] | None = source["content_categories"].values.tolist()
        else:
            groups = None

        # create item pool
        item_pool = ItemPool.load_from_list(a=a, b=b, c=c, d=d, ids=ids, content_categories=groups)

        # check if simulated responses are present
        if "simulated_responses" in source.columns:
            simulated_responses: List[int] = source["simulated_responses"].values.tolist() # type: ignore
            item_pool.simulated_responses = simulated_responses

        return item_pool
