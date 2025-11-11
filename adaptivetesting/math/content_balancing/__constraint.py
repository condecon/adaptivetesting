from dataclasses import dataclass


@dataclass
class Constraint:
    """Constraint for Exposure Constrol and Content Balancing
    """
    name: str
    """Constraint name. This string has to be the same
    in the associated items.
    """
    weight: float
    """Weight of this constraint.
    """
    prevalence: float
    """Frequency / Relative Frequency of a constraint and its items.
    For MPI, this value has to be an integer > 0.
    For WEP, this may be a float between 0 and 1.
    """
    lower: float | None = None
    """Lower bound of the constraint. Only required for WEP."""
    upper: float | None = None
    """Upper bound of the constraint. Only required for WEP."""
