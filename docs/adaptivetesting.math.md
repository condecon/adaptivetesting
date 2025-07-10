# math Module

### adaptivetesting.math.generate_response_pattern(ability: float, items: list[[TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)], seed: int | None = None) → list[int]

Generates a response pattern for a given ability level
and item difficulties. Also, a seed can be set.

Args:
: ability (float): participants ability
  items (list[TestItem]): test items
  seed (int, optional): Seed for the random process.

Returns:
: list[int]: response pattern

<a id="module-adaptivetesting.math.estimators"></a>

### *class* adaptivetesting.math.estimators.BayesModal(response_pattern: List[int] | ndarray, items: List[[TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)], prior: [Prior](#adaptivetesting.math.estimators.Prior), optimization_interval: Tuple[float, float] = (-10, 10))

Bases: [`IEstimator`](adaptivetesting.services.md#adaptivetesting.services.IEstimator)

This class can be used to estimate the current ability level
of a respondent given the response pattern and the corresponding
item difficulties.

This type of estimation finds the maximum of the posterior distribution.

Args:
: response_pattern (List[int] | np.ndarray ): list of response patterns (0: wrong, 1:right)
  <br/>
  items (List[TestItem]): list of answered items
  <br/>
  prior (Prior): prior distribution
  <br/>
  optimization_interval (Tuple[float, float]): interval used for the optimization function

#### get_estimation() → float

Estimate the current ability level using Bayes Modal.
If a NormalPrior is used, the bounded optimizer is used
to get the ability estimate.
For any other prior, it cannot be guaranteed that the optimizer will converge correctly.
Therefore, the full posterior distribution is calculated
and the maximum posterior value is selected.

Because this function uses a switch internally to determine
whether a optimizer is used for the estimate or not,
you have to create your custom priors from the correct base class (CustomPrior).
Otherwise, the estimate may not necessarily be correct!

Raises:
: AlgorithmException: Raised when maximum could not be found.
  CustomPriorException: Raised when custom prior is not based on the CustomPrior class.

Returns:
: float: ability estimation

#### get_standard_error(estimation: float) → float

Calculates the standard error for the given estimated ability level.

Args:
: estimation (float): currently estimated ability level

Returns:
: float: standard error of the ability estimation

### *class* adaptivetesting.math.estimators.CustomPrior(random_variable: rv_continuous, \*args: float, loc: float = 0, scale: float = 1)

Bases: [`Prior`](#adaptivetesting.math.estimators.Prior)

This class is for using a custom prior in the ability estimation
in Bayes Modal or Expected a Posteriori.
Any continous, univariate random variable from the scipy.stats module can be used.
However, you have to consult to the scipy documentation for the required parameters for
the probability density function (pdf) of that particular random variable.

Args:
: random_variable (rv_continuous): Any continous, univariate random variable from the scipy.stats module.
  <br/>
  ```
  *
  ```
  <br/>
  args (float): Custom parameters required to calculate the pdf of that specific random variable.
  <br/>
  loc (float, optional): Location parameter. Defaults to 0.
  <br/>
  scale (float, optional): Scale parameter. Defaults to 1.

#### pdf(x: float | ndarray) → ndarray

Probability density function for a prior distribution

Args:
: x (float | np.ndarray): point at which to calculate the function value

Returns:
: ndarray: function value

### *exception* adaptivetesting.math.estimators.CustomPriorException

Bases: `Exception`

This exception can be used is the custom prior
is not correctly specified.

It is usually raised if a non-normal prior is used
that was not correctly inherited from the CustomPrior class.

### *class* adaptivetesting.math.estimators.ExpectedAPosteriori(response_pattern: list[int] | ndarray, items: list[[TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)], prior: [Prior](#adaptivetesting.math.estimators.Prior), optimization_interval: tuple[float, float] = (-10, 10))

Bases: [`BayesModal`](#adaptivetesting.math.estimators.BayesModal)

This class can be used to estimate the current ability level
of a respondent given the response pattern and the corresponding
item difficulties.

This type of estimation finds the mean of the posterior distribution.

Args:
: response_pattern (List[int] | np.ndarray): list of response patterns (0: wrong, 1:right)
  <br/>
  items (List[TestItem]): list of answered items
  <br/>
  prior (Prior): prior distribution
  <br/>
  optimization_interval (Tuple[float, float]): interval used for the optimization function

#### get_estimation() → float

Estimate the current ability level using EAP.

Returns:
: float: ability estimation

#### get_standard_error(estimated_ability: float) → float

Calculates the standard error for the items used at the
construction of the class instance (answered items).
The currently estimated ability level is required as parameter.

Args:
: estimated_ability (float): \_description_

Raises:
: NotImplementedError: Either an instance of NormalPrior or CustomPrior has to be used.
  : If you want to use another calculation method for the standard,
    you have to specifically override this method.

Returns:
: float: standard error of the ability estimation

### *class* adaptivetesting.math.estimators.MLEstimator(response_pattern: List[int] | ndarray, items: List[[TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)], optimization_interval: Tuple[float, float] = (-10, 10), \*\*kwargs)

Bases: [`IEstimator`](adaptivetesting.services.md#adaptivetesting.services.IEstimator)

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

#### get_standard_error(estimation) → float

Calculates the standard error for the given estimated ability level.

Args:
: estimation (float): currently estimated ability level

Returns:
: float: standard error of the ability estimation

### *class* adaptivetesting.math.estimators.NormalPrior(mean: float, sd: float)

Bases: [`Prior`](#adaptivetesting.math.estimators.Prior)

Normal distribution as prior for Bayes Modal estimation

Args:
: mean (float): mean of the distribution
  <br/>
  sd (float): standard deviation of the distribution

#### pdf(x: float | ndarray) → ndarray

Probability density function for a prior distribution

Args:
: x (float | np.ndarray): point at which to calculate the function value

Returns:
: ndarray: function value

### *class* adaptivetesting.math.estimators.Prior

Bases: `ABC`

Base class for prior distributions

#### *abstractmethod* pdf(x: float | ndarray) → ndarray

Probability density function for a prior distribution

Args:
: x (float | np.ndarray): point at which to calculate the function value

Returns:
: ndarray: function value

### adaptivetesting.math.estimators.item_information_function(mu: ndarray, a: ndarray, b: ndarray, c: ndarray, d: ndarray) → ndarray

Calculate the information of a test item given the currently
estimated ability mu.

Args:
: mu (np.ndarray): currently estimated ability
  a (np.ndarray): \_description_
  b (np.ndarray): \_description_
  c (np.ndarray): \_description_
  d (np.ndarray): \_description_

Returns:
: np.ndarray: \_description_

### adaptivetesting.math.estimators.likelihood(mu: ndarray, a: ndarray, b: ndarray, c: ndarray, d: ndarray, response_pattern: ndarray) → ndarray

Likelihood function of the 4-PL model.
For optimization purposes, the function returns the negative value of the likelihood function.
To get the *real* value, multiply the result by -1.

Args:
: mu (np.ndarray): ability level
  <br/>
  a (np.ndarray): item discrimination parameter
  <br/>
  b (np.ndarray): item difficulty parameter
  <br/>
  c (np.ndarray): pseudo guessing parameter
  <br/>
  d (np.ndarray): inattention parameter

Returns:
: float: negative likelihood value of given ability value

### adaptivetesting.math.estimators.maximize_likelihood_function(a: ndarray, b: ndarray, c: ndarray, d: ndarray, response_pattern: ndarray, border: tuple[float, float] = (-10, 10)) → float

Find the ability value that maximizes the likelihood function.
This function uses the minimize_scalar function from scipy and the “bounded” method.

Args:
: a (np.ndarray): item discrimination parameter
  <br/>
  b (np.ndarray): item difficulty parameter
  <br/>
  c (np.ndarray): pseudo guessing parameter
  <br/>
  d (np.ndarray): inattention parameter
  <br/>
  response_pattern (np.ndarray): response pattern of the item
  border (tuple[float, float], optional): border of the optimization interval.
  Defaults to (-10, 10).

Raises:
: AlgorithmException: if the optimization fails or the response
  pattern consists of only one type of response.

Returns:
: float: optimized ability value

### adaptivetesting.math.estimators.maximize_posterior(a: ndarray, b: ndarray, c: ndarray, d: ndarray, response_pattern: ndarray, prior: [Prior](#adaptivetesting.math.estimators.Prior)) → float

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

### adaptivetesting.math.estimators.prior_information_function(prior: [Prior](#adaptivetesting.math.estimators.Prior), optimization_interval: tuple[float, float] = (-10, 10)) → ndarray

Calculates the fisher information for the probability density function
of the specified prior

Args:
: prior (Prior): \_description_

Returns:
: np.ndarray: \_description_

### adaptivetesting.math.estimators.probability_y0(mu: ndarray, a: ndarray, b: ndarray, c: ndarray, d: ndarray) → ndarray

Probability of getting the item wrong given the ability level.

Args:
: mu (np.ndarray): latent ability level
  <br/>
  a (np.ndarray): item discrimination parameter
  <br/>
  b (np.ndarray): item difficulty parameter
  <br/>
  c (np.ndarray): pseudo guessing parameter
  <br/>
  d (np.ndarray): inattention parameter

Returns:
: np.ndarray: probability of getting the item wrong

### adaptivetesting.math.estimators.probability_y1(mu: ndarray, a: ndarray, b: ndarray, c: ndarray, d: ndarray) → ndarray

Probability of getting the item correct given the ability level.

Args:
: mu (np.ndarray): latent ability level
  <br/>
  a (np.ndarray): item discrimination parameter
  <br/>
  b (np.ndarray): item difficulty parameter
  <br/>
  c (np.ndarray): pseudo guessing parameter
  <br/>
  d (np.ndarray): inattention parameter

Returns:
: np.ndarray: probability of getting the item correct

### adaptivetesting.math.estimators.test_information_function(mu: ndarray, a: ndarray, b: ndarray, c: ndarray, d: ndarray, prior: [Prior](#adaptivetesting.math.estimators.Prior) | None = None, optimization_interval: tuple[float, float] = (-10, 10)) → float

Calculates test information.
Therefore, the information is calculated for every item
and then summed up.
If a prior is specified, the fisher information of the prior
is calculated as well and added to the information sum.

Args:
: mu (np.ndarray): ability level
  a (np.ndarray): discrimination parameter
  b (np.ndarray): difficulty parameter
  c (np.ndarray): guessing parameter
  d (np.ndarray): slipping parameter

Returns:
: float: test information

<a id="module-adaptivetesting.math.item_selection"></a>

### adaptivetesting.math.item_selection.maximum_information_criterion(items: list[[TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)], ability: float) → [TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)

The maximum information criterion selected the next item for the respondent
by finding the item that has the highest information value.

Args:
: items (list[TestItem]): list of available items
  ability (float): currently estimated ability

Returns:
: TestItem: item that has the highest information value

Raises:
: ItemSelectionException: raised if no appropriate item was found
  AlgorithmException: raised if test information function could not be calculated

### adaptivetesting.math.item_selection.urrys_rule(items: List[[TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)], ability: float) → [TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)

Urry’s rule selects the test item
which has the minimal difference between
the item’s difficulty and the ability level.

Args:
: items (List[TestItem]): Test items (item pool)
  <br/>
  ability (float): Ability level (current ability estimation)

Returns:
: TestItem: selected test item
