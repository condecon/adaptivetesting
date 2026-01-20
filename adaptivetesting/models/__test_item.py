from typing import TypedDict

class TestItem:
    def __init__(self):
        """Representation of a test item in the item pool.
        The format is equal to the implementation in catR.

        Properties:
            - id (int | None): item ID
            - a (float): discrimination parameter
            - b (float | list[float]): difficulty parameter. For polytomous models, list of threshold parameters
            - c (float): guessing parameter. Ignored for polytomours models.
            - d (float): slipping parameter / upper asymptote. Ignored for polytomours models.
            - additional_properties (dict): addtional properties can be set if required.
                This functionality is used for content balancing.
                To use content balancing, set set `category` key of the class instance
                to a list of string which indicate the corresponding constraint classes.
                Example: `item.additional_properties["category"] = ["Math"]`

        """
        self.id: int | None = None
        self.a: float = 1
        self.b: float | list[float]= float("nan")
        self.c: float = 0
        self.d: float = 1
        self.additional_properties: dict = {}

    def as_dict(self, with_id = True):
        """Convert test item to a dictionary.

        Args:
            with_id (bool, optional): Deprecated. This argument will be ignored. 
                Defaults to True.

        """
        ItemDict = TypedDict("ItemDict", {
            "id": int | None,
            "a": float,
            "b": float | list[float],
            "c": float,
            "d": float,
            "additional_properties": dict
        })
        
        item_dict: ItemDict = {
            "id": self.id,
            "a": self.a,
            "b": self.b,
            "c": self.c,
            "d": self.d,
            "additional_properties": self.additional_properties
        }

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
