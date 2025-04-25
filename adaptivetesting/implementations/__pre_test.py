from typing import List
import jax.numpy as np
from ..models.__test_item import TestItem
import random


class PreTest:
    def __init__(self, items: List[TestItem], seed: int | None = None):
        """
        The pretest class can be used to draw items randomly from
        difficulty quantiles
        of the item pool.

        Args:
            items: Item pool

            seed (int): A seed for the item selection can be provided.
                If not, the item selection will be drawn randomly, and you will not be able
                to reproduce the results.

        """
        self.items = items
        self.seed = seed

    def calculate_quantiles(self) -> np.ndarray:
        """Calculates quantiles 0.25, 0.5, 0.75
        """
        # get difficulties
        difficulties: List[float] = [item.b for item in self.items]

        quantiles = np.array([])
        # calculate quantiles
        for q in [0.25, 0.5, 0.75]:
            quantile: np.ndarray = np.quantile(np.array(difficulties), q)
            quantiles = np.append(quantiles, quantile)

        return quantiles

    def select_item_in_interval(self, lower: float, upper: float) -> TestItem:
        """Draws item from a pool in the specified interval.
        The item difficulty is > than the lower limit and <= the higher limit.

        Args:
            lower (float): Lower bound of the item difficulty interval.
            
            upper (float): Upper bound of the item difficulty interval.

        Returns:
            TestItem: Selected item.
        """
        # select only items with difficulty in interval
        items_in_interval: List[TestItem] = [item for item in list(self.items)
                                             if lower < item.b <= upper]
        # draw one item randomly
        if self.seed is not None:
            random.seed(self.seed)
        item = random.sample(items_in_interval, 1)[0]
        return item

    def select_random_item_quantile(self) -> List[TestItem]:
        """Selects a random item from the 0.25, 0.5 and 0.75 quantiles.

        Returns:
            List[TestItem]: Selected item.
        """
        selected_items: List[TestItem] = []
        # create difficulties array
        difficulties = np.array([item.b for item in self.items])
        # add minimum and maximum difficulty values to
        # the quantiles list for correct item selection
        quantiles = [difficulties.min()]
        quantiles.extend(list(self.calculate_quantiles()))
        quantiles.extend([difficulties.max()])

        for i in range(len(quantiles) - 1):
            selected_item = self.select_item_in_interval(
                lower=float(quantiles[i]),
                upper=float(quantiles[i + 1]))

            selected_items.append(selected_item)

        # return
        return selected_items
