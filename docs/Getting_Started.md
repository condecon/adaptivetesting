# Getting Started

This small tutorial will give a general introduction to the package,
show the installation and how a small simulation is performed.

### 1. Package Installation

The package can be installed through `pip` or `conda` - depending on the user's
preference.
```bash
pip install adaptivetesting
```
or
```bash
conda install conda-forge::adaptivetesting
```

### 2. Load the items and set up the item pool
At first, the package should be imported. We recommend using a short alias, such as `adt`.
Then, the item pool can be loaded from a compatible format, such as a dictionary or simple lists.
In this example, we will load the item parameters from python lists.
```python
import adaptivetesting as adt
item_pool = adt.ItemPool.load_from_list(
    a = [0.42, 0.3, 1.5],
    b = [0.5, 0.9, 1.1]
)
```
Here, we use a 2PL model which is a simplified version of the 4PL model so that
the `c` and `d` parameters are not manually set but inferred by the package.

### 3. Define the adaptive test
The general adaptive testing procedure can be easily defined with the
`TestAssembler` class. This class supports numerous arguments to
also allow rather complex procedures.
For this example, we will only focus on a very basic configuration.

We configure a test for a single participant using ML for the ability estimation
and MFI for the item selection. Because we want to simulate the test later,
we have to specify a true ability level (here `0`) so that the package
may draw corresponding response patterns. For reproducibility, we also
set a seed (`123`).

```python
test = adt.TestAssembler(
    item_pool = item_pool,
    simulation_id="test",
    participant_id="1",
    ability_estimator=adt.MLEstimator,
    true_ability_level=0,
    seed=123
    )

```

### 4. Set up the simulation
The simulation can now simply be set up with the `Simulation` class.
Additionally, we have to specify a format in which the test results will be saved.
```python
simulation = adt.Simulation(test, adt.ResultOutputFormat.CSV)
```

### 5. Run the simulation
To start the actual simulation, we have to specify a stopping criterion.
We will use a standard error value of $0.4$ in this example.
```python
simulation.simulate(criterion=adt.StoppingCriterion.SE, value=0.4)
simulation.save_test_results()
```