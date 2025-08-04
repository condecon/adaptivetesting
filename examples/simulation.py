# flake8: noqa
import pandas as pd
previc_item_pool = pd.read_csv("item_pool.csv")
previc_item_pool.head()

from adaptivetesting.models import ItemPool
item_pool = ItemPool.load_from_list(
    b=previc_item_pool["Difficulty"]
)

from scipy.stats import norm
from numpy.random import seed
seed(1234)
theta_samples = norm.rvs(loc=0, scale=2, size=100)


from adaptivetesting.implementations import TestAssembler
from adaptivetesting.simulation import SimulationPool
from adaptivetesting.models import ResultOutputFormat, StoppingCriterion
from adaptivetesting.math.item_selection import maximum_information_criterion
from adaptivetesting.math.estimators import BayesModal, NormalPrior

tests = [
    TestAssembler(
        item_pool=item_pool,
        simulation_id="example_bm",
        participant_id=str(index),
        ability_estimator=BayesModal,
        estimator_args={
            "prior": NormalPrior(0,1),
            "optimization_interval":(-10, 10)
        },
        item_selector=maximum_information_criterion,
        true_ability_level=theta,
        simulation=True,
        seed=index
    )
    for index, theta in enumerate(theta_samples)
]

sim_pool = SimulationPool(
    adaptive_tests=tests,
    test_result_output=ResultOutputFormat.CSV,
    criterion=StoppingCriterion.SE,
    value=0.4
)
sim_pool.start()

import os

dfs = []
for i in range(100):
    filename = f"data/example_bm/{i}.csv"
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)
            # Get the last row of every file
            last_row = df.tail(1)
            dfs.append(last_row)
        # If there is an error, skip the file
        except Exception:
            pass
results_df = pd.concat(dfs, ignore_index=True)
mse = ((results_df["ability_estimation"] - results_df["true_ability_level"]) ** 2).mean()
print(f"MSE of ability estimates: {mse:.4f}")


import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.scatter(results_df["true_ability_level"],
           results_df["ability_estimation"],
           label="BM")
ax.plot(results_df["ability_estimation"],
        results_df["ability_estimation"],
        color="black")
ax.set_xlabel("True ability level")
ax.set_ylabel("Estimated ability level")
fig.savefig("sim_results_bm.pdf")

# other example
from adaptivetesting.math.estimators import ExpectedAPosteriori, CustomPrior
from scipy.stats.distributions import t

tests = [
    TestAssembler(
        item_pool=item_pool,
        simulation_id="example_eap",
        participant_id=str(index),
        ability_estimator=ExpectedAPosteriori,
        estimator_args={
            "prior": CustomPrior(t, 3),
            "optimization_interval":(-10, 10)
        },
        item_selector=maximum_information_criterion,
        true_ability_level=theta,
        simulation=True,
        seed=index
    )
    for index, theta in enumerate(theta_samples)
]

sim_pool = SimulationPool(
    adaptive_tests=tests,
    test_result_output=ResultOutputFormat.CSV,
    criterion=StoppingCriterion.SE,
    value=0.4
)
sim_pool.start()

dfs = []
for i in range(100):
    filename = f"data/example_eap/{i}.csv"
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)
            # Get the last row of every file
            last_row = df.tail(1)
            dfs.append(last_row)
        # If there is an error, skip the file
        except Exception:
            pass
results_df = pd.concat(dfs, ignore_index=True)
mse = ((results_df["ability_estimation"] - results_df["true_ability_level"]) ** 2).mean()
print(f"MSE of ability estimates: {mse:.4f}")


ax.scatter(results_df["true_ability_level"],
           results_df["ability_estimation"],
           label="EAP")
ax.set_xlabel("True ability level")
ax.set_ylabel("Estimated ability level")
ax.legend()
fig.savefig("sim_results_eap.pdf")
