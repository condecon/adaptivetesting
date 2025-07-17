from typing import Protocol, runtime_checkable
from ..models.__test_item import TestItem


@runtime_checkable
class ItemSelectionStrategy(Protocol):
    """
    A protocol for item selection strategies in adaptive testing.

    This protocol defines a callable interface for selecting a test item from a list of available items,
    given the current ability estimate and optional additional parameters.

    Args:
        
        items (list[TestItem]): The list of available test items to select from.
        
        ability (float): The current ability estimate of the test taker.
        
        **kwargs: Additional keyword arguments that may be required by specific selection strategies.

    Returns:
        TestItem: The selected test item based on the implemented strategy.
    """
    def __call__(self, items: list[TestItem], ability: float, **kwargs) -> TestItem:
        ...
