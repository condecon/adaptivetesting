from dataclasses import dataclass

@dataclass
class Constraint:
    name: str
    weight: float
    proportion: float
    lower: float | None = None
    upper: float | None = None