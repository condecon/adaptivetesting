from abc import abstractmethod


class BaseItem:
    def __init__(self):
        self.id: int | None
        self.a: float
        self.b: float | list[float]

    @abstractmethod
    def as_dict(self, with_id: bool = False):
        pass

    @staticmethod
    @abstractmethod
    def from_dict(source: dict) -> "BaseItem":
        pass


class TestItem(BaseItem):
    def __init__(self):
        """Representation of a test item in the item pool.
        The format is equal to the implementation in catR.

        Properties:
            - id (int | None): item ID
            - a (float): discrimination parameter
            - b (float): difficulty parameter
            - c (float): guessing parameter
            - d (float): slipping parameter / upper asymptote
            - additional_properties (dict): addtional properties can be set if required.
                This functionality is used for content balancing.
                To use content balancing, set set `category` key of the class instance
                to a list of string which indicate the corresponding constraint classes.
                Example: `item.additional_properties["category"] = ["Math"]`

        """
        self.id: int | None = None
        self.a: float = 1
        self.b: float = float("nan")
        self.c: float = 0
        self.d: float = 1
        self.additional_properties: dict = {}

    def as_dict(self, with_id: bool = False) -> dict[str, float | int | dict | None]:

        item_dict: dict[str, float | int | dict | None] = {
            "a": self.a,
            "b": self.b,
            "c": self.c,
            "d": self.d,
            "additional_properties": self.additional_properties
        }

        if with_id and self.id is not None:
            item_dict["id"] = self.id

        return item_dict
    
    @staticmethod
    def from_dict(source: dict) -> "TestItem":
        item = TestItem()
        # copy known fields, preserving defaults if keys are missing
        if "a" in source and source["a"] is not None:
            item.a = source["a"]
        if "b" in source and source["b"] is not None:
            item.b = source["b"]
        if "c" in source and source["c"] is not None:
            item.c = source["c"]
        if "d" in source and source["d"] is not None:
            item.d = source["d"]
        if "additional_properties" in source and source["additional_properties"] is not None:
            item.additional_properties = source["additional_properties"]
        if "id" in source and source["id"] is not None:
            item.id = source["id"]
        return item
        

class PolyItem(BaseItem):
    def __init__(self):
        self.id: int | None = None
        self.a: float = 1
        self.b: list[float] = [] # thresholds
        self.additional_properties: dict = {}
        self.num_categories: int = 2

    def as_dict(self, with_id=False):
        item_dict: dict[str, float | int | list | dict | None] = {
            "a": self.a,
            "b": self.b,
            "num_categories": self.num_categories,
            "additional_properties": self.additional_properties
        }
        if with_id and self.id is not None:
            item_dict["id"] = self.id
        return item_dict
    
    @staticmethod
    def from_dict(source) -> "PolyItem":
        item = PolyItem()
        if "a" in source and source["a"] is not None:
            item.a = source["a"]
        if "b" in source and source["b"] is not None:
            if not isinstance(source["b"], list):
                raise TypeError("b is not a list")
            item.b = source["b"]
        if "num_categories" in source and source["num_categories"] is not None:
            item.num_categories = source["num_categories"]
        if "additional_properties" in source and source["additional_properties"] is not None:
            if not isinstance(source["additional_properties"], dict):
                raise TypeError("additional_properties is not dict")
            item.additional_properties = source["additional_properties"]
        if "id" in source and source["id"] is not None:
            item.id = source["id"]

        return item
    
