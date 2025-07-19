from adaptivetesting.models import ItemPool
from adaptivetesting.implementations import TestAssembler
from adaptivetesting.math.estimators import BayesModal, NormalPrior
from adaptivetesting.simulation import Simulation, StoppingCriterion, ResultOutputFormat
import pandas as pd

# Create item pool from DataFrame
items_data = pd.DataFrame({
    "a": [1.32, 1.07, 0.84, 1.19, 0.95],  # discrimination
    "b": [-0.63, 0.18, -0.84, 0.41, -0.25],  # difficulty
    "c": [0.17, 0.10, 0.19, 0.15, 0.12],  # guessing
    "d": [0.87, 0.93, 1.0, 0.89, 0.94]   # upper asymptote
})
item_pool = ItemPool.load_from_dataframe(items_data)

# Set up adaptive test
adaptive_test = TestAssembler(
    item_pool=item_pool,
    simulation_id="sim_001",
    participant_id="participant_001",
    ability_estimator=BayesModal,
    estimator_args={"prior": NormalPrior(mean=0, sd=1)},
    true_ability_level=0.5,  # For simulation
    simulation=True
)

# Run simulation
simulation = Simulation(
    test=adaptive_test,
    test_result_output=ResultOutputFormat.CSV
)

simulation.simulate(
    criterion=StoppingCriterion.SE,
    value=0.3  # Stop when standard error <= 0.3
)

# Save results
simulation.save_test_results()