from psychopy import visual, event
from psychopy.hardware import keyboard
from adaptivetesting.implementations import TestAssembler
from adaptivetesting.models import AdaptiveTest, ItemPool, TestItem
from adaptivetesting.data import CSVContext
from adaptivetesting.math.estimators import BayesModal, CustomPrior
from adaptivetesting.math.item_selection import maximum_information_criterion
from scipy.stats import t


# Create item pool from DataFrame
items_data = pd.DataFrame({
    "a": [1.32, 1.07, 0.84, 1.19, 0.95],  # discrimination
    "b": [-0.63, 0.18, -0.84, 0.41, -0.25],  # difficulty
    "c": [0.17, 0.10, 0.19, 0.15, 0.12],  # guessing
    "d": [0.87, 0.93, 1.0, 0.89, 0.94]   # upper asymptote
})
item_pool = ItemPool.load_from_dataframe(items_data)

# Create adaptive test
adaptive_test: AdaptiveTest = TestAssembler(
        item_pool=item_pool,
        simulation_id="example",
        participant_id="dummy",
        ability_estimator=BayesModal,
        estimator_args={
            "prior": CustomPrior(t, 100),
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
    # get index
    item_difficulty: float = item.b
    stimuli: str = [item for item in items if item["Difficulty"] == item_difficulty][0]["word"]

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