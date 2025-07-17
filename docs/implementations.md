# implementations Module

## DefaultImplementation

### *class* adaptivetesting.implementations.DefaultImplementation(item_pool: [ItemPool](models.md#adaptivetesting.models.ItemPool), simulation_id: str, participant_id: int, true_ability_level: float, initial_ability_level: float = 0, simulation=True, debug=False)

Bases: [`AdaptiveTest`](models.md#adaptivetesting.models.AdaptiveTest)

This class represents the Default implementation using
Maximum Likelihood Estimation and Urry’s rule during the test.

Args:
: item_pool (ItemPool): item pool used for the test
  <br/>
  simulation_id (str): simulation id
  <br/>
  participant_id (int): participant id
  <br/>
  true_ability_level (float): true ability level (must always be set)
  <br/>
  initial_ability_level (float): initially assumed ability level
  <br/>
  simulation (bool): will the test be simulated
  <br/>
  debug (bool): enables debug mode

#### estimate_ability_level() → float

Estimates latent ability level using ML.
If responses are only 1 or 0,
the ability will be set to one
of the boundaries of the estimation interval ([-10,10]).

Returns:
: float: ability estimation

## PreTest

### *class* adaptivetesting.implementations.PreTest(items: List[[TestItem](models.md#adaptivetesting.models.TestItem)], seed: int | None = None)

Bases: `object`

The pretest class can be used to draw items randomly from
difficulty quantiles
of the item pool.

Args:
: items: Item pool
  <br/>
  seed (int): A seed for the item selection can be provided.
  : If not, the item selection will be drawn randomly, and you will not be able
    to reproduce the results.

#### calculate_quantiles() → Array

Calculates quantiles 0.25, 0.5, 0.75

#### select_item_in_interval(lower: float, upper: float) → [TestItem](models.md#adaptivetesting.models.TestItem)

Draws item from a pool in the specified interval.
The item difficulty is > than the lower limit and <= the higher limit.

Args:
: lower (float): Lower bound of the item difficulty interval.
  <br/>
  upper (float): Upper bound of the item difficulty interval.

Returns:
: TestItem: Selected item.

#### select_random_item_quantile() → List[[TestItem](models.md#adaptivetesting.models.TestItem)]

Selects a random item from the 0.25, 0.5 and 0.75 quantiles.

Returns:
: List[TestItem]: Selected item.

## SemiAdaptiveImplementation

### *class* adaptivetesting.implementations.SemiAdaptiveImplementation(item_pool: [ItemPool](models.md#adaptivetesting.models.ItemPool), simulation_id: str, participant_id: int, true_ability_level: float, initial_ability_level: float = 0, simulation=True, debug=False, pretest_seed=12345)

Bases: [`AdaptiveTest`](models.md#adaptivetesting.models.AdaptiveTest)

This class represents the Semi-Adaptive implementation using
Maximum Likelihood Estimation and Urry’s rule during the test.
The pretest is 4 items long.

Args:
: item_pool (ItemPool): item pool used for the test
  <br/>
  simulation_id (str): simulation id
  <br/>
  participant_id (int): participant id
  <br/>
  true_ability_level (float): true ability level (must always be set)
  <br/>
  initial_ability_level (float): initially assumed ability level
  <br/>
  simulation (bool): will the test be simulated
  <br/>
  debug (bool): enables debug mode
  <br/>
  pretest_seed (int): seed used for the random number generator to draw pretest items.

#### estimate_ability_level() → float

Estimates latent ability level using ML.
If responses are only 1 or 0,
the ability will be set to one
of the boundaries of the estimation interval ([-10,10]).

Returns:
: float: ability estimation

#### pre_test()

Runs pretest
