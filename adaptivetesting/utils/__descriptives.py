from ..models.__misc import ResultOutputFormat
import numpy as np
from .__funcs import load_final_test_results


def bias(simulation_id: str, participant_ids: list[str], output_format: ResultOutputFormat) -> np.floating:
    """
    Calculates the bias of ability estimations for a set of participants in a simulation.
    Bias is defined as the mean difference between estimated abilities and true ability levels.
    Args:
        simulation_id (str): Identifier for the simulation.
        participant_ids (list[str]): List of participant identifiers.
        output_format (ResultOutputFormat): Format in which the results are output.
    Returns:
        np.floating: The mean bias of ability estimations.
    """
    final_test_results = load_final_test_results(simulation_id, participant_ids, output_format)
    estimations = np.array([result.ability_estimation for result in final_test_results], dtype=np.float64)
    true_abilities = np.array([result.true_ability_level for result in final_test_results], dtype=np.float64)
    
    return np.mean(estimations - true_abilities)


def average_absolute_deviation(simulation_id: str,
                               participant_ids: list[str],
                               output_format: ResultOutputFormat) -> np.floating:
    """
    Calculates the average absolute deviation between estimated abilities
    and true ability levels for a set of participants.
    
    Args:
        simulation_id (str): Identifier for the simulation run.
        participant_ids (list[str]): List of participant identifiers.
        output_format (ResultOutputFormat): Format in which the results are returned.
    Returns:
        np.floating: The mean absolute deviation between estimated and true abilities.
    """
    final_test_results = load_final_test_results(simulation_id, participant_ids, output_format)
    estimations = np.array([result.ability_estimation for result in final_test_results], dtype=np.float64)
    true_abilities = np.array([result.true_ability_level for result in final_test_results], dtype=np.float64)

    return np.mean(np.abs(estimations - true_abilities))


def rmse(simulation_id: str,
         participant_ids: list[str],
         output_format: ResultOutputFormat) -> np.floating:
    """
    Calculates the root mean squared error (RMSE) between
    estimated abilities and true ability levels for a set of participants.
    
    Args:
        simulation_id (str): Identifier for the simulation run.
        participant_ids (list[str]): List of participant IDs to include in the calculation.
        output_format (ResultOutputFormat): Format in which the test results are returned.
    Returns:
        np.floating: The RMSE value between estimated and true abilities.
    """
    final_test_results = load_final_test_results(simulation_id, participant_ids, output_format)
    estimations = np.array([result.ability_estimation for result in final_test_results], dtype=np.float64)
    true_abilities = np.array([result.true_ability_level for result in final_test_results], dtype=np.float64)

    return np.sqrt(np.mean((estimations - true_abilities) ** 2))
