# implementations Module

### *class* adaptivetesting.implementations.DefaultImplementation(item_pool: [ItemPool](adaptivetesting.models.md#adaptivetesting.models.ItemPool), simulation_id: str, participant_id: str, true_ability_level: float, initial_ability_level: float = 0, simulation=True, debug=False)

Bases: [`AdaptiveTest`](adaptivetesting.simulation.md#adaptivetesting.simulation.AdaptiveTest)

This class represents the Default implementation using
Maximum Likelihood Estimation and Urry’s rule during the test.

Args:
: item_pool (ItemPool): item pool used for the test
  <br/>
  simulation_id (str): simulation id
  <br/>
  participant_id (str): participant id
  <br/>
  true_ability_level (float): true ability level (must always be set)
  <br/>
  initial_ability_level (float): initially assumed ability level
  <br/>
  simulation (bool): will the test be simulated
  <br/>
  debug (bool): enables debug mode

#### estimate_ability_level() → tuple[float, float]

Estimates latent ability level using ML.
If responses are only 1 or 0,
the ability will be set to one
of the boundaries of the estimation interval ([-10,10]).

Returns:
: (float, float): estimated ability level, standard error of the estimation

### *class* adaptivetesting.implementations.PreTest(items: List[[TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)], seed: int | None = None)

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

#### calculate_quantiles() → ndarray

Calculates quantiles 0.25, 0.5, 0.75

#### select_item_in_interval(lower: float, upper: float) → [TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)

Draws item from a pool in the specified interval.
The item difficulty is > than the lower limit and <= the higher limit.

Args:
: lower (float): Lower bound of the item difficulty interval.
  <br/>
  upper (float): Upper bound of the item difficulty interval.

Returns:
: TestItem: Selected item.

#### select_random_item_quantile() → List[[TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)]

Selects a random item from the 0.25, 0.5 and 0.75 quantiles.

Returns:
: List[TestItem]: Selected item.

### *class* adaptivetesting.implementations.SemiAdaptiveImplementation(item_pool: [ItemPool](adaptivetesting.models.md#adaptivetesting.models.ItemPool), simulation_id: str, participant_id: str, true_ability_level: float, initial_ability_level: float = 0, simulation=True, debug=False, pretest_seed=12345)

Bases: [`AdaptiveTest`](adaptivetesting.simulation.md#adaptivetesting.simulation.AdaptiveTest)

This class represents the Semi-Adaptive implementation using
Maximum Likelihood Estimation and Urry’s rule during the test.
The pretest is 4 items long.

Args:
: item_pool (ItemPool): item pool used for the test
  <br/>
  simulation_id (str): simulation id
  <br/>
  participant_id (str): participant id
  <br/>
  true_ability_level (float): true ability level (must always be set)
  <br/>
  initial_ability_level (float): initially assumed ability level. Default: 0.
  <br/>
  simulation (bool): will the test be simulated
  <br/>
  debug (bool): enables debug mode
  <br/>
  pretest_seed (int): seed used for the random number generator to draw pretest items.

#### estimate_ability_level() → tuple[float, float]

Estimates latent ability level using ML.
If responses are only 1 or 0,
the ability will be set to one
of the boundaries of the estimation interval ([-10,10]).

Returns:
: (float, float): estimated ability level, standard error of the estimation

#### pre_test()

Runs pretest

### *class* adaptivetesting.implementations.TestAssembler(item_pool, simulation_id, participant_id, ability_estimator: ~typing.Type[~adaptivetesting.services._\_estimator_interface.IEstimator], estimator_args: dict[str, ~typing.Any] = {'optimization_interval': (-10, 10), 'prior': None}, item_selector: ~adaptivetesting.services._\_item_selection_protocol.ItemSelectionStrategy = <function maximum_information_criterion>, item_selector_args: dict[str, ~typing.Any] = {}, pretest: bool = False, pretest_seed: int | None = None, true_ability_level=None, initial_ability_level=0, simulation=True, debug=False, \*\*kwargs)

Bases: [`AdaptiveTest`](adaptivetesting.simulation.md#adaptivetesting.simulation.AdaptiveTest)

TestAssembler is a subclass of AdaptiveTest designed to assemble and administer adaptive tests,
optionally including a pretest phase. It supports customizable ability estimation and item selection strategies.
Args:

> item_pool: The pool of test items available for selection.

> simulation_id: Identifier for the simulation run.

> participant_id: Identifier for the participant.

> ability_estimator (Type[IEstimator]): The estimator class used for ability estimation.

> estimator_args (dict[str, Any], optional):
> : Arguments for the ability estimator. Defaults to {“prior”: None, “optimization_interval”: (-10, 10)}.

> item_selector (ItemSelectionStrategy, optional):
> : Function or strategy for selecting the next item. Defaults to maximum_information_criterion.

> item_selector_args (dict[str, Any], optional): Arguments for the item selector. Defaults to {}.

> pretest (bool, optional): Whether to run a pretest phase before the main test. Defaults to False.

> pretest_seed (int | None, optional): Random seed for pretest item selection. Defaults to None.

> true_ability_level (optional): The true ability level of the participant (for simulation).

> initial_ability_level (optional): The initial ability estimate. Defaults to 0.

> simulation (bool, optional): Whether the test is run in simulation mode. Defaults to True.

> debug (bool, optional): Whether to enable debug output. Defaults to False.

> ```
> **
> ```

> kwargs: Additional keyword arguments passed to the AdaptiveTest superclass.

Methods:
: estimate_ability_level():
  : Estimates the current ability level using the specified estimator and handles exceptions
    for specific response patterns (all correct or all incorrect).
  <br/>
  get_next_item() -> TestItem:
  : Selects the next item to administer using the specified item selection strategy.
  <br/>
  run_test_once():
  : Runs a single iteration of the test, including an optional pretest phase. Handles item
    administration, response collection, ability estimation, and result recording.

Attributes:
: \_\_ability_estimator: The estimator class for ability estimation.
  <br/>
  \_\_estimator_args: Arguments for the ability estimator.
  <br/>
  \_\_item_selector: The item selection strategy.
  <br/>
  \_\_item_selector_args: Arguments for the item selector.
  <br/>
  \_\_pretest: Whether to run a pretest phase.
  <br/>
  \_\_pretest_seed: Random seed for pretest item selection.

Abstract implementation of an adaptive test.
All abstract methods have to be overridden
to create an instance of this class.

Abstract methods:
: - estimate_ability_level

Args:
: item_pool (ItemPool): item pool used for the test
  <br/>
  simulation_id (str): simulation id
  <br/>
  participant_id (str): participant id
  <br/>
  true_ability_level (float): true ability level (must always be set)
  <br/>
  initial_ability_level (float): initially assumed ability level
  <br/>
  simulation (bool): will the test be simulated.
  : If it is simulated and a response pattern is not yet set in the item pool,
    it will be generated for the given true ability level.
    A seed may also be set using the additional argument seed and set it to an int value, e.g.
    AdaptiveTest(…, seed=1234)
  <br/>
  DEBUG (bool): enables debug mode

#### estimate_ability_level()

Estimates the ability level of a test-taker based on their response pattern and answered items.
This method uses the configured ability estimator to calculate the ability estimation and its standard error.
If an AlgorithmException occurs during estimation,
and all responses are identical (all correct or all incorrect),
it assigns a default estimation value (-10 for all incorrect, 10 for all correct)
and recalculates the standard error.
Otherwise, it raises an AlgorithmException with additional context.

Returns:
: tuple[float, float]: A tuple containing the estimated ability level (float) and its standard error (float).

Raises:
: AlgorithmException: If estimation fails for reasons other than all responses being identical.

#### get_next_item() → [TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)

Selects and returns the next test item based on the current ability level and item selector strategy.

Returns:
: TestItem: The next item to be administered in the test, as determined by the item selector.

Raises:
: Any exceptions raised by the item selector function.

#### run_test_once()

Executes a single run of the test, including optional pretest logic.
If pretesting is enabled, this method:

> - Selects a random quantile of items from the item pool using a PreTest instance.
> - For each selected item:
>   : - Obtains a response (either simulated or real).
>     - Appends the response and item to the respective lists.
>     - Removes the item from the item pool.
> - Estimates the ability level and standard error after pretest responses.
> - Records test results for each pretest item, with the final item including the first ability estimation.

Returns:
: The result of the superclass’s run_test_once() method.
