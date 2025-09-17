class TestItem:
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
