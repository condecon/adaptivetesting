# models Module

## AdaptiveTest

### *class* adaptivetesting.models.AdaptiveTest(item_pool: [ItemPool](#adaptivetesting.models.ItemPool), simulation_id: str, participant_id: int, true_ability_level: float, initial_ability_level: float = 0, simulation: bool = True, DEBUG=False)

Bases: `ABC`

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
  participant_id (int): participant id
  <br/>
  true_ability_level (float): true ability level (must always be set)
  <br/>
  initial_ability_level (float): initially assumed ability level
  <br/>
  simulation (bool): will the test be simulated
  <br/>
  DEBUG (bool): enables debug mode

#### check_length_criterion(value: float) → bool

#### check_se_criterion(value: float) → bool

#### *abstractmethod* estimate_ability_level() → float

Estimates ability level.
The method has to be implemented by subclasses.

Returns:
: float: estimated ability level

#### get_ability_se() → float

Calculate the current standard error
of the ability estimation.

Returns:
: float: standard error of the ability estimation

#### get_answered_items() → List[[TestItem](#adaptivetesting.models.TestItem)]

Returns:
: List[TestItem]: answered items

#### get_answered_items_difficulties() → List[float]

Returns:
: List[float]: difficulties of answered items

#### get_item_difficulties() → List[float]

Returns:
: List[float]: difficulties of items in the item pool

#### get_next_item() → [TestItem](#adaptivetesting.models.TestItem)

Select next item using Urry’s rule.

Returns:
: TestItem: selected item

#### get_response(item: [TestItem](#adaptivetesting.models.TestItem)) → int

If the adaptive test is not used for simulation.
This method is used to get user feedback.

Args:
: item (TestItem): test item shown to the participant

Return:
: int: participant’s response

#### run_test_once()

Runs the test procedure once.
Saves the result to test_results of
the current instance.

## AlgorithmException

### *class* adaptivetesting.models.AlgorithmException

Bases: `Exception`

Exception that is thrown when the estimation process did not find a maximum.

## ItemPool

### *class* adaptivetesting.models.ItemPool(test_items: List[[TestItem](#adaptivetesting.models.TestItem)], simulated_responses: List[int] | None = None)

Bases: `object`

An item pool has to be created for an adaptive test.
For that, a list of test items has to be provided. If the package is used
to simulate adaptive tests, simulated responses have to be supplied as well.
The responses are matched to the items internally.
Therefore, both have to be in the same order.

Args:
: test_items (List[TestItem]): A list of test items. Necessary for any adaptive test.
  <br/>
  simulated_responses (List[int]): A list of simulated responses.
  Required for CAT simulations.

#### delete_item(item: [TestItem](#adaptivetesting.models.TestItem)) → None

Deletes item from item pool.
If simulated responses are defined, they will be deleted as well.

Args:
: item (TestItem): The test item to delete.

#### get_item_by_index(index: int) → Tuple[[TestItem](#adaptivetesting.models.TestItem), int] | [TestItem](#adaptivetesting.models.TestItem)

Returns item and if defined the simulated response.

Args:
: index (int): Index of the test item in the item pool to return.

Returns:
: TestItem or (TestItem, Simulated Response)

#### get_item_by_item(item: [TestItem](#adaptivetesting.models.TestItem)) → Tuple[[TestItem](#adaptivetesting.models.TestItem), int] | [TestItem](#adaptivetesting.models.TestItem)

Returns item and if defined the simulated response.

Args:
: item (TestItem): item to return.

Returns:
: TestItem or (TestItem, Simulated Response)

#### get_item_response(item: [TestItem](#adaptivetesting.models.TestItem)) → int

Gets the simulated response to an item if available.
A ValueError will be raised if a simulated response is not available.

Args:
: item (TestItem): item to get the corresponding response

Returns:
: (int): response (either 0 or 1)

#### *static* load_from_dataframe(source: DataFrame) → [ItemPool](#adaptivetesting.models.ItemPool)

Creates item pool from a pandas DataFrame.
Required columns are: a, b, c, d.
Each column has to contain float values.
A simulated_responses (int values) column can be added to
the DataFrame to provide simulated responses.

Args:
: source (DataFrame): \_description_

Returns:
: ItemPool: \_description_

#### *static* load_from_dict(source: dict[str, List[float]], simulated_responses: List[int] | None = None) → [ItemPool](#adaptivetesting.models.ItemPool)

Creates test items from a dictionary.
The dictionary has to have the following keys:

> - a
> - b
> - c
> - d

each containing a list of float.

Args:
: source (dict[str, List[float]]): item pool dictionary

Returns:
: List[TestItem]: item pool

#### *static* load_from_list(b: List[float], a: List[float] | None = None, c: List[float] | None = None, d: List[float] | None = None, simulated_responses: List[int] | None = None) → [ItemPool](#adaptivetesting.models.ItemPool)

Creates test items from a list of floats.

Args:
: a (List[float]): discrimination parameter
  <br/>
  b (List[float]): difficulty parameter
  <br/>
  c (List[float]): guessing parameter
  <br/>
  d (List[float]): slipping parameter
  <br/>
  simulated_responses (List[int]): simulated responses

Returns:
: List[TestItem]: item pool

## TestItem

### *class* adaptivetesting.models.TestItem

Bases: `object`

Representation of a test item in the item pool.
The format is equal to the implementation in catR.

Properties:
: - a (float):
  - b (float): difficulty
  - c (float):
  - d (float):

#### as_dict() → dict[str, float]

## TestResult

### *class* adaptivetesting.models.TestResult(test_id: str, ability_estimation: float, standard_error: float, showed_item: float, response: int, true_ability_level: float)

Bases: `object`

Representation of simulation test results

#### ability_estimation *: float*

#### *static* from_dict(dictionary: Dict) → [TestResult](#adaptivetesting.models.TestResult)

Create a TestResult from a dictionary

Args:
: dictionary: with the fields test_id, ability_estimation, standard_error, showed_item, response,
  true_ability_level

#### response *: int*

#### showed_item *: float*

#### standard_error *: float*

#### test_id *: str*

#### true_ability_level *: float*
