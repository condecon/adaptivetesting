from typing import Literal
from warnings import deprecated
from ..models.__test_item import TestItem
from ..models.__test_result import TestResult
from .__csv_context import CSVContext
from .__pickle_context import PickleContext


def read_prev_items(format: Literal["CSV", "PICKLE"],
                    test_id: str,
                    participant_ids: list[str]) -> list[TestItem]:
    """Read previously administered items
    to perform exposure control
    """
    all_shown_test_items = []
    
    for part_id in participant_ids:
        test_results = read_single_participant(test_id, part_id, format)
        items = [TestItem.from_dict(res.showed_item) for res in test_results]
        
        all_shown_test_items += items

    return all_shown_test_items


@deprecated("This function should be replaced after merging"
            " with revision branch")
def read_single_participant(test_id: str, participant_id: str, format: Literal["CSV", "PICKLE"]) -> list[TestResult]:
    context: CSVContext | PickleContext
    if format == "CSV":
        context = CSVContext(test_id, participant_id)
        return context.load()
    if format == "PICKLE":
        context = PickleContext(test_id, participant_id)
        return context.load()
