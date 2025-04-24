from typing import List
from psychopy import visual, event # type: ignore
from psychopy.hardware import keyboard # type: ignore
from adaptivetesting.implementations import DefaultImplementation
from adaptivetesting.models import AdaptiveTest, ItemPool, TestItem
from adaptivetesting.data import PickleContext

# ====================
# Adaptive Test Setup
# ====================

# create example items (difficulties)
item_difficulties: List[float] = [-3,
                                  -2.5,
                                  -1.24,
                                  0.2,
                                  0.5,
                                  0.7,
                                  1,
                                  2]

# convert to test items
items: List[TestItem] = ItemPool.load_from_list(item_difficulties).test_items

# create example stimuli
item_stimuli: List[str] = ["A",
                           "B",
                           "C",
                           "D",
                           "E",
                           "F",
                           "G",
                           "H"]

# create item_pool
item_pool: ItemPool = ItemPool(
    test_items=items,
    simulated_responses=None
)

# create adaptive test
adaptive_test: AdaptiveTest = DefaultImplementation(
    item_pool=item_pool,
    simulation_id="0",
    participant_id=0,
    true_ability_level=None, # type: ignore
    simulation=False
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
    # get index
    index: int = item_difficulties.index(item.b)
    stimuli: str = item_stimuli[index]

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


# override adaptive test standard function
adaptive_test.get_response = get_response # type: ignore

# start adaptive test
while True:
    adaptive_test.run_test_once()

    # check stopping criterion
    if adaptive_test.get_ability_se() <= 0.4:
        break

    # end test if all items have been shown
    if len(adaptive_test.item_pool.test_items) == 0:
        break

# save test results
data_context = PickleContext(
    adaptive_test.simulation_id,
    adaptive_test.participant_id
)

data_context.save(adaptive_test.test_results)
