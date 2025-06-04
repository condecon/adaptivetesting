from ...models.__test_item import TestItem
from ...models.__item_selection_exception import ItemSelectionException
from ..estimators.__test_information import test_information_function
from ..estimators.__prior import Prior
from ...models.__algorithm_exception import AlgorithmException
import jax.numpy as jnp


def maximum_information_criterion(items: list[TestItem],
                                  ability: float,
                                  prior: Prior | None = None,
                                  optimization_interval: tuple[float, float] = (-10, 10)) -> TestItem:
    """The maximum information criterion selected the next item for the respondent
    by finding the item that maximizes the test information function.

    Args:
        items (list[TestItem]): list of available items
        ability (float): currently estimated ability

    Returns:
        TestItem: item that maximizes the test information function

    Raises:
        ItemSelectionException: raised if no appropriate item was found
        AlgorithmException: raised if test information function could not be calculated
    """
    max_information = float("-inf")
    best_item = None

    for item in items:
        # extract parameters from the current item
        a = jnp.array([item.a])
        b = jnp.array([item.b])
        c = jnp.array([item.c])
        d = jnp.array([item.d])

        # calculate test information for the current item
        try:
            information = test_information_function(
                mu=jnp.array([ability], dtype=float),
                a=a,
                b=b,
                c=c,
                d=d,
                prior=prior,
                optimization_interval=optimization_interval
            )
            
            # if information is higher than before
            # set the item as new best item
            if information > max_information:
                max_information = information
                best_item = item
        except Exception as e:
            raise AlgorithmException(f"Error calculating test information: {e}")
        
    if best_item is None:
        raise ItemSelectionException("No appropriate item could be selected.")
    
    return best_item
