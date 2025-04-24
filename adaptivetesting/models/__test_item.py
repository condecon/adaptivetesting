class TestItem:
    def __init__(self):
        """Representation of a test item in the item pool.
        The format is equal to the implementation in catR.

        Properties:
            - a (float):
            - b (float): difficulty
            - c (float):
            - d (float):

        """
        self.id: int | None = None
        self.a: float = 1
        self.b: float = float("nan")
        self.c: float = 0
        self.d: float = 1
    
    def as_dict(self) -> dict[str, float]:
        return {
            "a": self.a,
            "b": self.b,
            "c": self.c,
            "d": self.d
        }
