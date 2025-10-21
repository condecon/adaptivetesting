import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure, SubFigure
from ..models.__misc import ResultOutputFormat
from ..models.__test_item import TestItem
from ..math.estimators.__functions.__estimators import probability_y1
from ..math.estimators.__test_information import item_information_function
from .__funcs import load_final_test_results, load_test_results_single_participant
import numpy as np


def plot_final_ability_estimates(simulation_id: str,
                                 participant_ids: list[str],
                                 output_format: ResultOutputFormat,
                                 ax: Axes | None = None, **kwargs):
    """
    Plots the final ability estimates against the true ability levels for a set of participants in a simulation.
    Args:
        simulation_id (str): Identifier for the simulation whose results are to be plotted.
        participant_ids (list[str]): List of participant IDs to include in the plot.
        output_format (ResultOutputFormat): Format in which the results are stored and should be read.
        ax (Axes | None, optional): Matplotlib Axes object to plot on. If None, a new figure and axes are created.
        **kwargs: Additional keyword arguments passed to `ax.scatter`.
    Returns:
        tuple: (fig, ax) where `fig` is the Matplotlib Figure object and `ax` is the Axes object containing the plot.
    Notes:
        - The function reads the final test results for the specified participants and simulation.
        - It plots the estimated ability levels against the true ability levels using a scatter plot.
    """
    # get old attributes
    fig: Figure | SubFigure
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    # read final test results data
    final_test_results = load_final_test_results(simulation_id, participant_ids, output_format)
    # extract true and finally estimated ability levels
    true_and_final_abilities = [
        (result.ability_estimation, result.true_ability_level)
        for result in final_test_results
    ]

    final_estimates, true_abilities = zip(*true_and_final_abilities)
    
    if "color" not in kwargs:
        ax.scatter(true_abilities, final_estimates, color="blue", **kwargs)
    else:
        ax.scatter(true_abilities, final_estimates, **kwargs)
    ax.plot(true_abilities, true_abilities, color="black")
    ax.set_xlabel("True ability level")
    ax.set_ylabel("Estimated ability level")

    return fig, ax


def plot_icc(item: TestItem,
             range: tuple[float, float] = (-10, 10),
             ax: Axes | None = None,
             **kwargs):
    """
    Plots the Item Characteristic Curve (ICC) for a given test item.
    Parameters:
        item (TestItem): The test item containing parameters (a, b, c, d) for the ICC.
        range (tuple[float, float], optional): The range of ability levels (theta) to plot. Defaults to (-10, 10).
        ax (Axes, optional): Matplotlib Axes object to plot on. If None, a new figure and axes are created.
        **kwargs: Additional keyword arguments passed to matplotlib's plot function.
    Returns:
        tuple: A tuple containing the matplotlib Figure and Axes objects.
    """
    thetas = np.linspace(range[0], range[1], 1000)
    probabilities = probability_y1(
        mu=np.array(thetas).T,
        a=np.array(item.a),
        b=np.array(item.b),
        c=np.array(item.c),
        d=np.array(item.d),
    )

    fig: Figure | SubFigure
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    # create plot
    ax.plot(thetas, probabilities, **kwargs)
    ax.set_xlabel("Ability level")
    ax.set_ylabel("Probability of correct response")

    return fig, ax
  

def plot_iif(item: TestItem,
             range: tuple[float, float] = (-10, 10),
             ax: Axes | None = None,
             **kwargs):
    """
    Plots the Item Information Function (IIF) for a given test item over a specified ability range.
    Parameters:
        item (TestItem): The test item for which to plot the information function.
        range (tuple[float, float], optional): The range of ability levels (theta) to plot over. Defaults to (-10, 10).
        ax (Axes, optional): Matplotlib Axes object to plot on. If None, a new figure and axes are created.
        **kwargs: Additional keyword arguments passed to matplotlib's plot function.
    Returns:
        tuple[Figure, Axes]: The matplotlib Figure and Axes objects containing the plot.
    """
    # calculate item information
    thetas = np.linspace(range[0], range[1], 100)
    information_array = item_information_function(
        mu=np.array(thetas).T,
        a=np.array(item.a),
        b=np.array(item.b),
        c=np.array(item.c),
        d=np.array(item.d),
    )

    # setup figure
    fig: Figure | SubFigure
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    ax.plot(thetas, information_array, **kwargs)
    ax.set_xlabel("Ability level")
    ax.set_ylabel("Item information")
    return fig, ax


def plot_exposure_rate(simulation_id: str,
                       participant_ids: list[str],
                       output_format: ResultOutputFormat):
    """This function returns the exposure rates for all shown items
    in a series of adaptive tests or CAT simulations.

    Args:
        simulation_id (str): Simulation identifyer
        participant_ids (list[str]): List of unique participant IDs
        output_format (ResultOutputFormat): Format in which the test results have been previously saved

    Returns:
        tuple[Figure, Axes]: matplotlib figure and axes
    """
    # read test results for each participant and collect shown item ids
    all_item_ids: list[str] = []
    for participant in participant_ids:
        test_results = load_test_results_single_participant(
            simulation_id=simulation_id,
            participant_id=participant,
            output_format=output_format,
        )

        # each TestResult has a 'showed_item' dict with an 'id' key
        participant_item_ids = [res.showed_item["id"] for res in test_results]
        all_item_ids.extend(participant_item_ids)

    if len(all_item_ids) == 0:
        # nothing to plot, return empty figure
        fig, ax = plt.subplots()
        ax.set_title("No items shown - no exposure data")
        return fig, ax

    # unique item ids and counts
    unique_ids, counts = np.unique(np.array(all_item_ids, dtype=object), return_counts=True)

    # sort by counts descending for better readability
    order = np.argsort(counts)[::-1]
    unique_ids_sorted = unique_ids[order]
    counts_sorted = counts[order]

    # compute exposure percentage relative to number of participants (or total exposures)
    total_exposures = len(all_item_ids)
    exposure_pct = counts_sorted / total_exposures * 100.0

    # create bar plot
    fig, ax = plt.subplots(figsize=(max(6, len(unique_ids_sorted) * 0.2), 4))
    bars = ax.bar(range(len(unique_ids_sorted)), counts_sorted, tick_label=unique_ids_sorted)
    ax.set_xlabel("Item id")
    ax.set_ylabel("Times shown")
    ax.set_title("Item exposure counts (sorted)")
    plt.xticks(rotation=90)

    # annotate bars with percentage labels
    for rect, pct in zip(bars, exposure_pct):
        height = rect.get_height()
        ax.annotate(f"{pct:.1f}%",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    fig.tight_layout()
    return fig, ax


def plot_test_information(
        items: list[TestItem],
        range: tuple[float, float] = (-10, 10),
        ax: Axes | None = None,
        **kwargs):
    """
    Plots the Item Information Function (IIF) for a given test item over a specified ability range.
    Args:
        items (list[TestItem]): Test items in an item pool for which to calculate the test information
        range (tuple[float, float], optional): The range of ability levels (theta) to plot over. Defaults to (-10, 10).
        ax (Axes, optional): Matplotlib Axes object to plot on. If None, a new figure and axes are created.
        **kwargs: Additional keyword arguments passed to matplotlib's plot function.
    Returns:
        tuple[Figure, Axes]: The matplotlib Figure and Axes objects containing the plot.
    """
    # calculate test information by summing item information across items
    thetas = np.linspace(range[0], range[1], 100)
    information_array = np.zeros_like(thetas, dtype=float)
    for item in items:
        information_array += item_information_function(
            mu=np.array(thetas).T,
            a=np.array(item.a),
            b=np.array(item.b),
            c=np.array(item.c),
            d=np.array(item.d),
        )

    # setup figure
    fig: Figure | SubFigure
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    ax.plot(thetas, information_array, **kwargs)
    ax.set_xlabel("Ability level")
    ax.set_ylabel("Test information")
    return fig, ax


def plot_theta_estimation_trace(simulation_id: str,
                                participant_id: str,
                                output_format: ResultOutputFormat,
                                ax: Axes | None = None,):
    """
    Plot the time (step) trace of true ability levels and estimated abilities for a single participant.
    This function loads per-item test results for the given simulation and participant using
    load_test_results_single_participant, extracts the true ability levels and the model's
    ability estimations at each step, and renders a two-line plot showing how the estimated
    ability evolves relative to the true ability across test steps.
    
    Args:
        simulation_id (str): Identifier of the simulation run to load results from.
        participant_id (str): Identifier of the participant whose results will be plotted.
        output_format (ResultOutputFormat)
            Format or storage hint forwarded to load_test_results_single_participant to control
            how results are retrieved/returned.
        ax (Axes (optional)): matplotlib axis object. If None is passed to the function,
            an Axes object is created internally.
    
    
    Returns:
        tuple[Figure, Axes]:A tuple containing the Matplotlib Figure and Axes objects with the rendered plot.
        The plot includes:
        - a black line for "True ability" (true_ability_level per step)
        - a blue line for "Ability Estimations" (ability_estimation per step)
        The x-axis corresponds to the sequential test step index.
    """
    test_results = load_test_results_single_participant(
        simulation_id=simulation_id,
        participant_id=participant_id,
        output_format=output_format
    )

    true_abilities = np.array([
        result.true_ability_level
        for result in test_results
    ])

    estimations = np.array([
        result.ability_estimation
        for result in test_results
    ])

    steps = np.array(range(len(test_results)))

    # setup figure
    fig: Figure | SubFigure
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    ax.plot(steps, true_abilities, label="True ability", color="black")
    ax.plot(steps, estimations, label="Ability Estimations", color="blue")
    ax.legend()

    return fig, ax
