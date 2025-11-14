from typing import Callable, Any
import random
import numpy as np
from .__exposure_control import ExposureControl
from ...models.__adaptive_test import AdaptiveTest
from ...models.__test_item import TestItem
from ..estimators.__test_information import item_information_function



class Randomesque(ExposureControl):
    def __init__(self,
                 adaptive_test: AdaptiveTest,
                 n_items: int,
                 seed: int | None = None,
                 reverse: bool = True):
        """
        Exposure Control using randomesque item selection.
        Instead of the most informative item, the `n` most informative items are selected.
        From this selection, the final item is drawn randomly. For this process, a seed
        can be specified.

        Args:
            adaptive_test (AdaptiveTest): instance of the adaptive test
            n_items (int): number of items to select
            seed (int | None): random seed for the final item selection
            reverse (bool): If `True` the most informative items are selected. Default `True`.


        References
        ------------
        Kingsbury, C. G., & Zara, A. R. (1991). A Comparison of Procedures for Content-Sensitive
        Item Selection in Computerized Adaptive Tests. Applied Measurement in Education, 4(3), 241–261.
        Psychology and Behavioral Sciences Collection. https://doi.org/10.1207/s15324818ame0403_4

        Kingsbury, G. G., & Zara, A. R. (1989). Procedures for selecting items for
        computerized adaptive tests. Applied Measurement in Education, 2(4), 359–375.

        """
        super().__init__(adaptive_test)

        # extract items
        self.items = adaptive_test.item_pool.test_items
        self.ability_estimate = adaptive_test.ability_level
        self.n_items = n_items
        self.seed = seed
        self.reverse = reverse

    def select_item(self) -> TestItem:
        """Select an item based on the implemented selection rules

        Returns:
            TestItem | None: selected test item
        """
        selected_items = self.radomesque_item_selection(
            self.items,
            self.ability_estimate,
            self.n_items,
            self.reverse,
            self.sort_by_information,
            self.seed
        )
        return selected_items

    @staticmethod
    def sort_by_information(item_entry: tuple[float, int]) -> float:
        """
        Internal function for sorting items by their information value

        Args:
            item_entry: tuple of information value and item index

        Returns:
            information value of given item
        """
        return item_entry[0]


    @staticmethod
    def radomesque_item_selection(items: list[TestItem],
            ability_estimate: float,
            n_items: int,
            reverse: bool = True,
            item_rating_function: Callable = item_information_function,
            seed: int | None = None,
            **kwargs: Any
    ) -> TestItem:
        item_information_list: list[tuple[float, int]] = []
        for i, item in enumerate(items):
            information = float(item_rating_function(
                a=np.array(item.a),
                b=np.array(item.b),
                c=np.array(item.c),
                d=np.array(item.d),
                mu=np.array(ability_estimate),
                **kwargs
            ))

            item_information_list.append((information, i))

        # sort items in ascending order to have the first item be the one with the highest
        # information value (default or expected settings)
        item_information_list.sort(key=Randomesque.sort_by_information, reverse=reverse)

        # select first n items
        selected_items = item_information_list[0:n_items]
        # select only items
        sub_item_pool = [items[item[1]] for item in selected_items]

        # randomly select items from sub item pool
        if seed is not None:
            random.seed(seed)
        sampled_item = random.sample(sub_item_pool, k=1)[0]
        return sampled_item
