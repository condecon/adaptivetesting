# adaptivetesting

<img src="/docs/source/_static/logo.svg" style="width: 100%">
</img>

**An open-source Python package for simplified, customizable Computerized Adaptive Testing (CAT) using Bayesian methods.**


## Key Features

- **Bayesian Methods**: Built-in support for Bayesian ability estimation with customizable priors
- **Flexible Architecture**: Object-oriented design with abstract classes for easy extension
- **Item Response Theory**: Full support for 1PL, 2PL, 3PL, and 4PL models
- **Multiple Estimators**:
  - Maximum Likelihood Estimation (MLE)
  - Bayesian Modal Estimation (BM)
  - Expected A Posteriori (EAP)
- **Item Selection Strategies**: Kaximum information criterion and Urry's rule
- **Simulation Framework**: Comprehensive tools for CAT simulation and evaluation
- **Real-world Application**: Direct transition from simulation to production testing
- **Stopping Criteria**: Support for standard error and test length criteria
- **Data Management**: Built-in support for CSV and pickle data formats

## Installation

Install from PyPI using pip:

```bash
pip install adaptivetesting
```

For the latest development version:

```bash
pip install git+https://github.com/condecon/adaptivetesting
```

## Requirements

- Python >= 3.10
- NumPy >= 2.0.0
- Pandas >= 2.2.0
- SciPy >= 1.15.0
- tqdm >= 4.67.1

## Quick Start

### Basic Example: Setting Up an Adaptive Test

```python
from adaptivetesting.models import ItemPool, TestItem
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
```

### Custom Prior Example

```python
from adaptivetesting.math.estimators import CustomPrior
from scipy.stats import t

# Create custom t prior
custom_prior = CustomPrior(t, 100)

# Use in estimator
adaptive_test = TestAssembler(
    item_pool=item_pool,
    simulation_id="custom_prior_sim",
    participant_id="participant_002",
    ability_estimator=BayesModal,
    estimator_args={"prior": custom_prior},
    true_ability_level=0.0,
    simulation=True
)
```

### Real-world Testing (Non-simulation) with PsychoPy

```python
# setup item pool
# the item pool is retrieved from the PREVIC
# https://github.com/manuelbohn/previc/tree/main/saves
import pandas as pd
from adaptivetesting.models import ItemPool
from psychopy import visual, event
from psychopy.hardware import keyboard
from adaptivetesting.implementations import TestAssembler
from adaptivetesting.models import AdaptiveTest, ItemPool, TestItem
from adaptivetesting.data import CSVContext
from adaptivetesting.math.estimators import ExpectedAPosteriori, CustomPrior
from adaptivetesting.math.item_selection import maximum_information_criterion
from scipy.stats import t
import pandas as pd

previc_item_pool = pd.read_csv("item_pool.csv")
# add item column
previc_item_pool["id"] = list(range(1, 90))
previc_item_pool.head()


item_pool = ItemPool.load_from_list(
    b=previc_item_pool["Difficulty"],
    ids=previc_item_pool["id"]
)

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

## FIX THIS

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
```

## Package Structure

The package is organized into several key modules:

- **`adaptivetesting.models`**: Core classes including `AdaptiveTest`, `ItemPool`, and `TestItem`
- **`adaptivetesting.implementations`**: Ready-to-use test implementations like `TestAssembler`
- **`adaptivetesting.math`**: Mathematical functions for IRT, ability estimation, and item selection
- **`adaptivetesting.simulation`**: Simulation framework and result management
- **`adaptivetesting.data`**: Data management utilities for CSV and pickle formats
- **`adaptivetesting.services`**: Abstract interfaces and protocols

## Advanced Features

### Multiple Stopping Criteria

```python
simulation.simulate(
    criterion=[StoppingCriterion.SE, StoppingCriterion.LENGTH],
    value=[0.3, 20]  # Stop at SE ≤ 0.3 OR length ≥ 20 items
)
```

### Pretest Phase

```python
adaptive_test = TestAssembler(
    item_pool=item_pool,
    simulation_id="pretest_sim",
    participant_id="participant_003",
    ability_estimator=BayesModal,
    estimator_args={"prior": NormalPrior(0, 1)},
    pretest=True,
    pretest_seed=42,
    simulation=True
)
```

### Custom Item Selection

```python
from adaptivetesting.math.item_selection import maximum_information_criterion

adaptive_test = TestAssembler(
    item_pool=item_pool,
    simulation_id="custom_selection",
    participant_id="participant_004",
    ability_estimator=BayesModal,
    estimator_args={"prior": NormalPrior(0, 1)},
    item_selector=maximum_information_criterion,
    item_selector_args={"additional_param": "value"},
    simulation=True
)
```

### Custom Optimization Interval
```python
adaptive_test = TestAssembler(
    item_pool=item_pool,
    simulation_id="pretest_sim",
    participant_id="participant_003",
    ability_estimator=BayesModal,
    estimator_args={
        "prior": NormalPrior(0, 1),
        "optimization_interval": (-5, 5)},
    pretest_seed=42,
    simulation=True
)
```

## Documentation

Full documentation is available in the `docs/` directory:

- [API Reference](docs/readme.md)
- [Models Module](docs/models.md)
- [Math Module](docs/math.md)
- [Implementation Examples](docs/implementations.md)
- [Simulation Guide](docs/simulation.md)

## Testing

The package includes comprehensive tests. Run them using:

```bash
uv sync
uv run python -m unittest
```

## Contributing

We welcome contributions! Please see our [GitHub repository](https://github.com/condecon/adaptivetesting) for:

- Issue tracking
- Feature requests
- Pull request guidelines
- Development setup

## Research and Applications

This package is designed for researchers and practitioners in:

- Educational assessment
- Psychological testing
- Cognitive ability measurement
- Adaptive learning systems
- Psychometric research

The package facilitates the transition from research simulation to real-world testing applications without requiring major code modifications.

## Citation
If you use this package for your academic work, please provide the following reference:
Engicht, J., Bee, R. M., & Koch, T. (2025). Customizable Bayesian Adaptive Testing with Python – The adaptivetesting Package. Open Science Framework. https://doi.org/10.31219/osf.io/d2xge_v1

```
@online{engichtCustomizableBayesianAdaptive2025,
  title = {Customizable {{Bayesian Adaptive Testing}} with {{Python}} – {{The}} Adaptivetesting {{Package}}},
  author = {Engicht, Jonas and Bee, R. Maximilian and Koch, Tobias},
  date = {2025-08-06},
  eprinttype = {Open Science Framework},
  doi = {10.31219/osf.io/d2xge_v1},
  url = {https://osf.io/d2xge_v1},
  pubstate = {prepublished}
}
```

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.
