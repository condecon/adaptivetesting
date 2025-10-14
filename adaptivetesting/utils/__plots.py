import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure, SubFigure
from ..models.__misc import ResultOutputFormat
from ..models.__test_item import TestItem
from ..math.estimators.__functions.__estimators import probability_y1
from .__funcs import load_final_test_results
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
  

def plot_iif():
    pass


def plot_exposure_rate():
    pass


def plot_test_information():
    pass


def plot_theta_estimation_trace():
    pass
