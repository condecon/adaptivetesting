# services Module

## IEstimator

### *class* adaptivetesting.services.IEstimator(response_pattern: List[int] | Array, items: List[[TestItem](models.md#adaptivetesting.models.TestItem)], optimization_interval: Tuple[float, float] = (-10, 10))

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

## ITestResults

### *class* adaptivetesting.services.ITestResults(simulation_id: str, participant_id: int)

Bases: `ABC`

Interface for saving and reading test results.
This interface may mainly be used for saving simulation results.

Args:
: simulation_id (str): The simulation ID. Name of the results file.
  <br/>
  participant_id (int): The participant ID.

#### *abstractmethod* load() → List[[TestResult](models.md#adaptivetesting.models.TestResult)]

#### *abstractmethod* save(test_results: List[[TestResult](models.md#adaptivetesting.models.TestResult)]) → None
