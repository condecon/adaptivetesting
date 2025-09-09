# flake8: noqa
# setup item pool
# the item pool is retrieved from the PREVIC
# https://github.com/manuelbohn/previc/tree/main/saves
import pandas as pd
previc_item_pool = pd.read_csv("item_pool.csv")
# add item column
previc_item_pool["id"] = list(range(1, 90))
previc_item_pool.head()

from adaptivetesting.models import ItemPool
item_pool = ItemPool.load_from_list(
    b=previc_item_pool["Difficulty"],
    ids=previc_item_pool["id"]
)

# import psychopy
from psychopy import visual, event
from psychopy.hardware import keyboard
from adaptivetesting.implementations import TestAssembler
from adaptivetesting.models import AdaptiveTest, ItemPool, TestItem
from adaptivetesting.data import CSVContext
from adaptivetesting.math.estimators import ExpectedAPosteriori, CustomPrior
from adaptivetesting.math.item_selection import maximum_information_criterion
from scipy.stats import t
import pandas as pd

# Create adaptive test
adaptive_test: AdaptiveTest = TestAssembler(
        item_pool=item_pool,
        simulation_id="example",
        participant_id="dummy",
        ability_estimator=ExpectedAPosteriori,
        estimator_args={
            "prior": CustomPrior(t, 3),
            "optimization_interval":(-10, 10)
        },
        item_selector=maximum_information_criterion,
        simulation=False,
        debug=False
)

# ====================
# Setup PsychoPy
# ====================

# general setup
win = visual.Window([800, 600],
                    monitor="testMonitor",
                    units="deg",
                    fullscr=False)

# init keyboard
keyboard.Keyboard()


# define function to get user input
def get_response(item: TestItem) -> int:
    # select corresponding word from item pool data frame
    stimuli: str = previc_item_pool[previc_item_pool["id"] == item.id]["word"].values[0]

    # create text box and display stimulus
    text_box = visual.TextBox2(win=win,
                               text=stimuli,
                               alignment="center",
                               size=24)
    # draw text
    text_box.draw()
    # update window
    win.flip()

    # wait for pressed keys
    while True:
        keys = event.getKeys()
        # if keys are not None
        if keys:
            # if the right arrow keys is pressed
            # return 1
            if keys[0] == "right":
                return 1
            # if the left arrow keys is pressed
            # return 0
            if keys[0] == "left":
                return 0


# override adaptive test default function
adaptive_test.get_response = get_response

# start adaptive test
while True:
    adaptive_test.run_test_once()

    # check stopping criterion
    if adaptive_test.standard_error <= 0.4:
        break

    # end test if all items have been shown
    if len(adaptive_test.item_pool.test_items) == 0:
        break

# save test results
data_context = CSVContext(
    adaptive_test.simulation_id,
    adaptive_test.participant_id
)

data_context.save(adaptive_test.test_results)