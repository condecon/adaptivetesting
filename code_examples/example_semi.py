from typing import List
from adaptivetesting.models import TestItem, ItemPool, AdaptiveTest,load_test_items_from_list
from adaptivetesting.implementations import SemiAdaptiveImplementation
from adaptivetesting.simulation import Simulation, ResultOutputFormat, StoppingCriterion

# =================
# Data Setup
# =================

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
items: List[TestItem] = load_test_items_from_list(item_difficulties)

# create simulated responses
simulated_responses: List[int] = [1,
                                  1,
                                  1,
                                  0,
                                  1,
                                  0,
                                  0,
                                  0]

# instantiate item pool
item_pool: ItemPool = ItemPool(
    test_items=items,
    simulated_responses=simulated_responses
)

# =================
# Simulation Setup
# =================

# create adaptive test using the Default implementation
# the required values simulation_id (str) and participant_id (int)
# are set to "default" and 0 and can be freely chosen
adaptive_test: AdaptiveTest = SemiAdaptiveImplementation(
    item_pool=item_pool,
    simulation_id="semi",
    participant_id=0,
    true_ability_level=0, # example value, must always be set
    initial_ability_level=0, # not used but inheritance requirement
    simulation=True,
    pretest_seed=12345 # pretest for the random item selection in the pretest
)

# setup simulation using PICKLE as the result output format
simulation: Simulation = Simulation(
    test=adaptive_test,
    test_result_output=ResultOutputFormat.PICKLE
)

# =================
# Start Simulation
# =================

# use standard error as stopping criterion
simulation.simulate(
    criterion=StoppingCriterion.SE,
    value=0.4
)

# =================
# Save Simulation
# =================

# save simulation results
simulation.save_test_results()