from typing import Callable, Any
import random
import numpy as np
from ...models.__test_item import TestItem
from ..estimators.__test_information import item_information_function


def radomesque_item_selection(
        items: list[TestItem],
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

    def sort_by_information(item_entry: tuple[float, int]) -> float:
        return item_entry[0]
    
    # sort items in ascending order to have the first item be the one with the hightest
    # information value (default or expected settings)
    item_information_list.sort(key=sort_by_information, reverse=reverse)

    # select first n items
    selected_items = item_information_list[0:n_items]
    # select only items
    sub_item_pool = [items[item[1]] for item in selected_items]
    
    # randomly select items from sub item pool
    if seed is not None:
        random.seed(seed)
    sampled_item = random.sample(sub_item_pool, k=1)[0]
    return sampled_item
