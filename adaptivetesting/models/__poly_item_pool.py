from .__item_pool import ItemPool
from ..models.__test_item import PolyItem
from .__base_item_pool import BaseItemPool
from pandas import DataFrame


# TODO: Static load functions
# TODO: replace in assembler
class PolyItemPool(BaseItemPool):
    def __init__(self,
                 test_items: list[PolyItem],
                 simulated_responses: list[int] | None = None):

        self.test_items: list[PolyItem] = test_items
        self.simulated_responses: list[int] | None = simulated_responses

    @staticmethod
    def load_from_list(a: list[float],
                       b: list[list[float]],
                       simulated_responses: list[int] | None = None,
                       ids: list[int] | None = None,
                       content_categories: list[list[str]] | None = None) -> "PolyItemPool":
        items: list[PolyItem] = []
        
        if len(a) != len(b):
            raise ValueError("Length of a and b has to be the same.")
        
        for i in range(len(a)):
            item = PolyItem()
            item.a = a[i]
            item.b = b[i]
            items.append(item)

        if content_categories is not None:
            if len(content_categories) != len(b):
                raise ValueError("Length of content_categories and b has to be the same.")
            for i, groups in enumerate(content_categories):
                items[i].additional_properties["category"] = groups

        item_pool = PolyItemPool(item, simulated_responses)
        return item_pool

    @staticmethod
    def load_from_dict(source, simulated_responses = None, ids = None, content_categories = None):
        """Creates test items from a dictionary.
        The dictionary has to have the following keys:

            - a
            - b

        each containing a list of float.
        """
        a = source.get("a")
        b = source.get("b")

        # check none
        if a is None:
            raise ValueError("a cannot be None")

        if b is None:
            raise ValueError("b cannot be None")
        
        # check if a, b, c, and d have the same length
        if not len(a) == len(b):
            raise ValueError("All lists in the source dictionary must have the same length")
        
        if ids is not None:
            if len(ids) != len(b):
                raise ValueError("Length of ids and b has to be the same.")

        if content_categories is not None:
            if len(content_categories) != len(b):
                raise ValueError("Length of content_categories and b has to be the same.")
            
        n_items = len(b)
        items: list[PolyItem] = []
        for i in range(n_items):
            item = PolyItem()
            item.a = a[i]
            item.b = b[i]

            if ids is not None:
                item.id = ids[i]
            if content_categories is not None:
                item.additional_properties["category"] = content_categories[i]

            items.append(item)

        item_pool = PolyItemPool(items, simulated_responses)
        return item_pool


    @staticmethod
    def load_from_dataframe(source: DataFrame) -> "ItemPool":
        """Creates item pool from a pandas DataFrame.
        Required columns are: `a`, `b`.
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

        if "c" not in source.columns:
            raise ValueError("Column 'c' not found.")

        if "d" not in source.columns:
            raise ValueError("Column 'd' not found.")

        # get values
        a: list[float] = source["a"].values.tolist() # type: ignore
        b: list[float] = source["b"].values.tolist() # type: ignore

        if "ids" in source.columns:
            ids: List[int] | None = source["ids"].values.tolist() # type: ignore
        else:
            ids = None

        if "content_categories" in source.columns:
            groups: list[list[str]] | None = source["content_categories"].values.tolist()
        else:
            groups = None

        # create item pool
        item_pool = ItemPool.load_from_list(a=a, b=b, ids=ids, content_categories=groups)

        # check if simulated responses are present
        if "simulated_responses" in source.columns:
            simulated_responses: list[int] = source["simulated_responses"].values.tolist() # type: ignore
            item_pool.simulated_responses = simulated_responses
        return item_pool

    
    