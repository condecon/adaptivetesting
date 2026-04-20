from typing import Literal
from warnings import deprecated
from ..models.__test_item import TestItem
from ..models.__test_result import TestResult
from .__csv_context import CSVContext
from .__pickle_context import PickleContext


def read_prev_items(format: Literal["CSV", "PICKLE"],
                    test_id: str,
                    participant_ids: list[str]) -> list[TestItem]:
    """Read previously administered items.
    This function is internally used to perform exposure control.

    Args:
        format (Literal["CSV", "PICKLE"]): The format of the results: CSV or PICKLE.
        test_id (str): The test ID / simulation ID.
        participant_ids (list[str]): The participant IDs.

    Returns:
        list[TestItem]: A list of TestItem objects.
    """
    all_shown_test_items = []
    
    for part_id in participant_ids:
        test_results = read_single_participant(test_id, part_id, format)
        items = [TestItem.from_dict(res.showed_item) for res in test_results]
        
        all_shown_test_items += items

    return all_shown_test_items


@deprecated("This function will be removed in future releases.")
def read_single_participant(test_id: str, participant_id: str, format: Literal["CSV", "PICKLE"]) -> list[TestResult]:
    """
    Reads the test results of a particular participant.
    Args:
        test_id (str): The test ID / simulation ID.
        participant_id (str): The participant ID.
        format (Literal["CSV", "PICKLE"]): The format of the results: CSV or PICKLE.

    Returns:
        list[TestResult]: A list of TestResult objects.

    Raises:
        ValueError: If the format is not supported.
    """
    context: CSVContext | PickleContext
    if format == "CSV":
        context = CSVContext(test_id, participant_id)
        return context.load()
    if format == "PICKLE":
        context = PickleContext(test_id, participant_id)
        return context.load()
    raise ValueError(f"Unknown format: {format}")
