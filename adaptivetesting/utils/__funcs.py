from ..models.__test_result import TestResult
from ..data.__csv_context import CSVContext
from ..data.__pickle_context import PickleContext
from ..services.__test_results_interface import ITestResults
from ..models.__misc import ResultOutputFormat


def load_final_test_results(simulation_id: str,
                            participant_ids: list[str],
                            output_format: ResultOutputFormat) -> list[TestResult]:
    """
    Loads the final test results for a list of participants from the specified simulation or adaptive test.
    Depending on the output format (CSV or PICKLE), this function initializes the appropriate context,
    loads all test results for each participant, and selects the final result (assumed to be the last entry).
    The final results are collected and returned as a list.
    Args:
        simulation_id (str): The identifier for the simulation from which to load results.
        participant_ids (list[str]): A list of participant IDs whose results are to be loaded.
        output_format (ResultOutputFormat): The format in which results are stored (CSV or PICKLE).
    Returns:
        list[TestResult]: A list containing the final test result for each participant.
    Raises:
        ValueError: If the output_format is not set to either ResultOutputFormat.CSV or ResultOutputFormat.PICKLE.
    """
    # load data
    final_test_results: list[TestResult] = []
    context: ITestResults

    if output_format is ResultOutputFormat.CSV:
        for id in participant_ids:
            context = CSVContext(simulation_id, participant_id=id)
            test_results = context.load()
            # select final result
            final_result = test_results[-1]
            final_test_results.append(final_result)

    if output_format is ResultOutputFormat.PICKLE:
        for id in participant_ids:
            context = PickleContext(simulation_id, participant_id=id)
            test_results = context.load()
            # select final result
            final_result = test_results[-1]
            final_test_results.append(final_result)
    else:
        raise ValueError("output_format is not correctly set to either PICKLE of CSV.")

    return final_test_results