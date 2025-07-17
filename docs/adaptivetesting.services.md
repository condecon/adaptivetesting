# services Module

### *class* adaptivetesting.services.IEstimator(response_pattern: List[int] | ndarray, items: List[[TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)], optimization_interval: Tuple[float, float] = (-10, 10))

Bases: `ABC`

This is the interface required for every possible
estimator.
Any estimator inherits from this class and implements
the get_estimation method.

Args:
: response_pattern (List[int]): list of responses (0: wrong, 1:right)
  <br/>
  items (List[TestItem]): list of answered items

#### *abstractmethod* get_estimation() → float

Get the currently estimated ability.

Returns:
: float: ability

#### *abstractmethod* get_standard_error(estimation: float) → float

Calculates the standard error for the given estimated ability level.

Args:
: estimation (float): currently estimated ability level

Returns:
: float: standard error of the ability estimation

### *class* adaptivetesting.services.ITestResults(simulation_id: str, participant_id: str)

Bases: `ABC`

Interface for saving and reading test results.
This interface may mainly be used for saving simulation results.

Args:
: simulation_id (str): The simulation ID. Name of the results file.
  <br/>
  participant_id (str): The participant ID.

#### *abstractmethod* load() → List[[TestResult](adaptivetesting.models.md#adaptivetesting.models.TestResult)]

#### *abstractmethod* save(test_results: List[[TestResult](adaptivetesting.models.md#adaptivetesting.models.TestResult)]) → None

### *class* adaptivetesting.services.ItemSelectionStrategy(\*args, \*\*kwargs)

Bases: `Protocol`

A protocol for item selection strategies in adaptive testing.

This protocol defines a callable interface for selecting a test item from a list of available items,
given the current ability estimate and optional additional parameters.

Args:

> items (list[TestItem]): The list of available test items to select from.

> ability (float): The current ability estimate of the test taker.

> ```
> **
> ```

> kwargs: Additional keyword arguments that may be required by specific selection strategies.

Returns:
: TestItem: The selected test item based on the implemented strategy.
