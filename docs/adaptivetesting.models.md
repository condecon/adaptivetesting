# models Module

### *class* adaptivetesting.models.AdaptiveTest(item_pool: [ItemPool](#adaptivetesting.models.ItemPool), simulation_id: str, participant_id: str, true_ability_level: float | None = None, initial_ability_level: float = 0, simulation: bool = True, DEBUG=False, \*\*kwargs)

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

#### \_\_init_\_(item_pool: [ItemPool](#adaptivetesting.models.ItemPool), simulation_id: str, participant_id: str, true_ability_level: float | None = None, initial_ability_level: float = 0, simulation: bool = True, DEBUG=False, \*\*kwargs)

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

#### check_length_criterion(value: float) → bool

#### check_se_criterion(value: float) → bool

#### *abstractmethod* estimate_ability_level() → tuple[float, float]

Estimates ability level.
The method has to be implemented by subclasses.

Returns:
: (float, float): estimated ability level, standard error of the estimation

#### get_answered_items() → List[[TestItem](#adaptivetesting.models.TestItem)]

Returns:
: List[TestItem]: answered items

#### get_answered_items_difficulties() → List[float]

Returns:
: List[float]: difficulties of answered items

#### get_item_difficulties() → List[float]

Returns:
: List[float]: difficulties of items in the item pool

#### *abstractmethod* get_next_item() → [TestItem](#adaptivetesting.models.TestItem)

Select next item.

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

### *exception* adaptivetesting.models.AlgorithmException

Bases: `Exception`

Exception that is thrown when the estimation process did not find a maximum.

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

#### \_\_init_\_(test_items: List[[TestItem](#adaptivetesting.models.TestItem)], simulated_responses: List[int] | None = None)

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

### *exception* adaptivetesting.models.ItemSelectionException(\*args)

Bases: `Exception`

#### \_\_init_\_(\*args)

### *class* adaptivetesting.models.ResultOutputFormat(\*values)

Bases: `Enum`

Enum for selecting the output format for
the test results

#### CSV *= 1*

#### PICKLE *= 2*

### *class* adaptivetesting.models.StoppingCriterion(\*values)

Bases: `Enum`

Enum for selecting the stopping criterion
for the adaptive test

#### LENGTH *= 2*

#### SE *= 1*

### *class* adaptivetesting.models.TestItem

Bases: `object`

Representation of a test item in the item pool.
The format is equal to the implementation in catR.

Properties:
: - a (float):
  - b (float): difficulty
  - c (float):
  - d (float):

#### \_\_init_\_()

Representation of a test item in the item pool.
The format is equal to the implementation in catR.

Properties:
: - a (float):
  - b (float): difficulty
  - c (float):
  - d (float):

#### as_dict() → dict[str, float]

### *class* adaptivetesting.models.TestResult(test_id: str, ability_estimation: float, standard_error: float, showed_item: dict, response: int, true_ability_level: float)

Bases: `object`

Representation of simulation test results

#### \_\_init_\_(test_id: str, ability_estimation: float, standard_error: float, showed_item: dict, response: int, true_ability_level: float) → None

#### ability_estimation *: float*

#### *static* from_dict(dictionary: Dict) → [TestResult](#adaptivetesting.models.TestResult)

Create a TestResult from a dictionary

Args:
: dictionary: with the fields test_id, ability_estimation, standard_error, showed_item, response,
  true_ability_level

#### response *: int*

#### showed_item *: dict*

#### standard_error *: float*

#### test_id *: str*

#### true_ability_level *: float*
