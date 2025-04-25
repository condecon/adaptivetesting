# math Module

## Estimators

### MLEstimator

### *class* adaptivetesting.math.estimators.MLEstimator(response_pattern: List[int] | Array, items: List[[TestItem](models.md#adaptivetesting.models.TestItem)], optimization_interval: Tuple[float, float] = (-10, 10))

Bases: [`IEstimator`](services.md#adaptivetesting.services.IEstimator)

This class can be used to estimate the current ability level
of a respondent given the response pattern and the corresponding
item parameters.
The estimation uses Maximum Likelihood Estimation.

Args:
: response_pattern (List[int]): list of response patterns (0: wrong, 1:right)
  <br/>
  items (List[TestItem]): list of answered items

#### get_estimation() → float

Estimate the current ability level by searching
for the maximum of the likelihood function.
A line-search algorithm is used.

Returns:
: float: ability estimation

### Prior

### *class* adaptivetesting.math.estimators.Prior

Bases: `ABC`

Base class for prior distributions

#### *abstractmethod* pdf(x: float | Array) → Array

Probability density function for a prior distribution

Args:
: x (float | np.ndarray): point at which to calculate the function value

Returns:
: ndarray: function value

### NormalPrior

### *class* adaptivetesting.math.estimators.NormalPrior(mean: float, sd: float)

Bases: [`Prior`](#adaptivetesting.math.estimators.Prior)

Normal distribution as prior for Bayes Modal estimation

Args:
: mean (float): mean of the distribution
  <br/>
  sd (float): standard deviation of the distribution

#### pdf(x: float | Array) → Array

Probability density function for a prior distribution

Args:
: x (float | np.ndarray): point at which to calculate the function value

Returns:
: ndarray: function value

### probability_y1

### adaptivetesting.math.estimators.probability_y1(mu: Array, a: Array, b: Array, c: Array, d: Array) → Array

Probability of getting the item correct given the ability level.

Args:
: mu (jnp.ndarray): latent ability level
  <br/>
  a (jnp.ndarray): item discrimination parameter
  <br/>
  b (jnp.ndarray): item difficulty parameter
  <br/>
  c (jnp.ndarray): pseudo guessing parameter
  <br/>
  d (jnp.ndarray): inattention parameter

Returns:
: jnp.ndarray: probability of getting the item correct

### probability_y0

### adaptivetesting.math.estimators.probability_y0(mu: Array, a: Array, b: Array, c: Array, d: Array) → Array

Probability of getting the item wrong given the ability level.

Args:
: mu (jnp.ndarray): latent ability level
  <br/>
  a (jnp.ndarray): item discrimination parameter
  <br/>
  b (jnp.ndarray): item difficulty parameter
  <br/>
  c (jnp.ndarray): pseudo guessing parameter
  <br/>
  d (jnp.ndarray): inattention parameter

Returns:
: jnp.ndarray: probability of getting the item wrong

### maximize_likelihood_function

### adaptivetesting.math.estimators.maximize_likelihood_function(a: Array, b: Array, c: Array, d: Array, response_pattern: Array, border: tuple[float, float] = (-10, 10)) → float

Find the ability value that maximizes the likelihood function.
This function uses the minimize_scalar function from scipy and the “bounded” method.

Args:
: a (jnp.ndarray): item discrimination parameter
  <br/>
  b (jnp.ndarray): item difficulty parameter
  <br/>
  c (jnp.ndarray): pseudo guessing parameter
  <br/>
  d (jnp.ndarray): inattention parameter
  <br/>
  response_pattern (jnp.ndarray): response pattern of the item
  border (tuple[float, float], optional): border of the optimization interval.
  Defaults to (-10, 10).

Raises:
: AlgorithmException: if the optimization fails or the response
  pattern consists of only one type of response.

Returns:
: float: optimized ability value

### likelihood

### adaptivetesting.math.estimators.likelihood(mu: Array, a: Array, b: Array, c: Array, d: Array, response_pattern: Array) → Array

Likelihood function of the 4-PL model.
For optimization purposes, the function returns the negative value of the likelihood function.
To get the *real* value, multiply the result by -1.

Args:
: mu (jnp.ndarray): ability level
  <br/>
  a (jnp.ndarray): item discrimination parameter
  <br/>
  b (jnp.ndarray): item difficulty parameter
  <br/>
  c (jnp.ndarray): pseudo guessing parameter
  <br/>
  d (jnp.ndarray): inattention parameter

Returns:
: float: likelihood value of given ability value

### maximize_posterior

### adaptivetesting.math.estimators.maximize_posterior(a: Array, b: Array, c: Array, d: Array, response_pattern: Array, prior: [Prior](#adaptivetesting.math.estimators.Prior)) → float

\_summary_

Args:
: a (np.ndarray): \_description_
  <br/>
  b (np.ndarray): \_description_
  <br/>
  c (np.ndarray): \_description_
  <br/>
  d (np.ndarray): \_description_
  <br/>
  response_pattern (np.ndarray): \_description_
  <br/>
  prior (Prior): \_description_

Returns:
: float: Bayes Modal estimator for the given parameters

## Item Selection

### urrys_rule

### adaptivetesting.math.item_selection.urrys_rule(items: List[[TestItem](models.md#adaptivetesting.models.TestItem)], ability: float) → [TestItem](models.md#adaptivetesting.models.TestItem)

Urry’s rule selects the test item
which has the minimal difference between
the item’s difficulty and the ability level.

Args:
: items (List[TestItem]): Test items (item pool)
  <br/>
  ability (float): Ability level (current ability estimation)

Returns:
: TestItem: selected test item

## standard_error

### adaptivetesting.math.standard_error(answered_items: List[[TestItem](models.md#adaptivetesting.models.TestItem)], estimated_ability_level: float, estimator: Literal['ML', 'BM'] = 'ML', sd: float | None = None) → float

Calculates the standard error using the test information function.
If Bayes Modal is used for the ability estimation, a standard deviation value
of the prior distribution has to be provided.

Args:
: answered_items (List[float]): List of answered items
  <br/>
  estimated_ability_level (float): Currently estimated ability level
  <br/>
  estimator (Literal[“ML”, “BM”]): Ability estimator (Default: ML)
  <br/>
  sd (float | None): Standard deviation of the prior distribution. Only required for BM.

Raises:
: ValueError

Returns:
: float: Standard error

## test_information_function

### adaptivetesting.math.test_information_function(mu: Array, a: Array, b: Array, c: Array, d: Array) → float

Calculates test information.

Args:
: mu (np.ndarray): ability level
  a (np.ndarray): discrimination parameter
  b (np.ndarray): difficulty parameter
  c (np.ndarray): guessing parameter
  d (np.ndarray): slipping parameter

Returns:
: float: test information

## Utilities

### generate_response_pattern

### adaptivetesting.math.generate_response_pattern(ability: float, items: list[[TestItem](models.md#adaptivetesting.models.TestItem)], seed: int | None = None) → list[int]

Generates a response pattern for a given ability level
and item difficulties. Also, a seed can be set.

Args:
: ability (float): participants ability
  items (list[TestItem]): test items
  seed (int, optional): Seed for the random process.

Returns:
: list[int]: response pattern
