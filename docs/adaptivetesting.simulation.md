# simulation Module

### *class* adaptivetesting.simulation.AdaptiveTest(item_pool: [ItemPool](adaptivetesting.models.md#adaptivetesting.models.ItemPool), simulation_id: str, participant_id: str, true_ability_level: float | None = None, initial_ability_level: float = 0, simulation: bool = True, DEBUG=False, \*\*kwargs)

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

#### check_length_criterion(value: float) → bool

#### check_se_criterion(value: float) → bool

#### *abstractmethod* estimate_ability_level() → tuple[float, float]

Estimates ability level.
The method has to be implemented by subclasses.

Returns:
: (float, float): estimated ability level, standard error of the estimation

#### get_answered_items() → List[[TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)]

Returns:
: List[TestItem]: answered items

#### get_answered_items_difficulties() → List[float]

Returns:
: List[float]: difficulties of answered items

#### get_item_difficulties() → List[float]

Returns:
: List[float]: difficulties of items in the item pool

#### *abstractmethod* get_next_item() → [TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)

Select next item.

Returns:
: TestItem: selected item

#### get_response(item: [TestItem](adaptivetesting.models.md#adaptivetesting.models.TestItem)) → int

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

### *class* adaptivetesting.simulation.CSVContext(simulation_id: str, participant_id: str)

Bases: [`ITestResults`](#adaptivetesting.simulation.ITestResults)

Implementation of the ITestResults interface for
saving test results to the CSV format.
The resulting CSV file <participant_id>.csv
will be a standard comma-separated values file.

Args:
: simulation_id (str): folder name
  <br/>
  participant_id (str): participant id

#### load() → List[[TestResult](adaptivetesting.models.md#adaptivetesting.models.TestResult)]

Loads results from the database.
The implementation of this method is required
by the interface. However, it does not have
any implemented functionality and will throw an error
if used.

Returns: List[TestResult]

#### save(test_results: List[[TestResult](adaptivetesting.models.md#adaptivetesting.models.TestResult)]) → None

Saves a list of test results to a CSV file
(<participant_id>.csv).

Args:
: test_results (List[TestResult]): list of test results

### *class* adaptivetesting.simulation.ITestResults(simulation_id: str, participant_id: str)

Bases: `ABC`

Interface for saving and reading test results.
This interface may mainly be used for saving simulation results.

Args:
: simulation_id (str): The simulation ID. Name of the results file.
  <br/>
  participant_id (str): The participant ID.

#### *abstractmethod* load() → List[[TestResult](adaptivetesting.models.md#adaptivetesting.models.TestResult)]

#### *abstractmethod* save(test_results: List[[TestResult](adaptivetesting.models.md#adaptivetesting.models.TestResult)]) → None

### *class* adaptivetesting.simulation.PickleContext(simulation_id: str, participant_id: str)

Bases: [`ITestResults`](#adaptivetesting.simulation.ITestResults)

Implementation of the ITestResults interface for
saving test results to the pickle format.
The resulting pickle file <simulation_id>.pickle
will be of the standard pickle format which depends
on the used python version.

Args:
: simulation_id (str): folder name
  <br/>
  participant_id (str): participant id

#### load() → List[[TestResult](adaptivetesting.models.md#adaptivetesting.models.TestResult)]

Loads results from the database.
The implementation of this method is required
by the interface. However, is does not have
any implemented functionality and will throw an error
if used.

Returns: List[TestResult]

#### save(test_results: List[[TestResult](adaptivetesting.models.md#adaptivetesting.models.TestResult)]) → None

Saves a list of test results to a pickle binary file
(<participant_id>.pickle).

Args:
: test_results (List[TestResult]): list of test results

### *class* adaptivetesting.simulation.ProcessPoolExecutor(max_workers=None, mp_context=None, initializer=None, initargs=(), , max_tasks_per_child=None)

Bases: `Executor`

Initializes a new ProcessPoolExecutor instance.

Args:
: max_workers: The maximum number of processes that can be used to
  : execute the given calls. If None or not given then as many
    worker processes will be created as the machine has processors.
  <br/>
  mp_context: A multiprocessing context to launch the workers created
  : using the multiprocessing.get_context(‘start method’) API. This
    object should provide SimpleQueue, Queue and Process.
  <br/>
  initializer: A callable used to initialize worker processes.
  initargs: A tuple of arguments to pass to the initializer.
  max_tasks_per_child: The maximum number of tasks a worker process
  <br/>
  > can complete before it will exit and be replaced with a fresh
  > worker process. The default of None means worker process will
  > live as long as the executor. Requires a non-‘fork’ mp_context
  > start method. When given, we default to using ‘spawn’ if no
  > mp_context is supplied.

#### map(fn, \*iterables, timeout=None, chunksize=1)

Returns an iterator equivalent to map(fn, iter).

Args:
: fn: A callable that will take as many arguments as there are
  : passed iterables.
  <br/>
  timeout: The maximum number of seconds to wait. If None, then there
  : is no limit on the wait time.
  <br/>
  chunksize: If greater than one, the iterables will be chopped into
  : chunks of size chunksize and submitted to the process pool.
    If set to one, the items in the list will be sent one at a time.

Returns:
: An iterator equivalent to: map(func, 
  <br/>
  ```
  *
  ```
  <br/>
  iterables) but the calls may
  be evaluated out-of-order.

Raises:
: TimeoutError: If the entire result iterator could not be generated
  : before the given timeout.
  <br/>
  Exception: If fn(
  <br/>
  ```
  *
  ```
  <br/>
  args) raises for any values.

#### shutdown(wait=True, , cancel_futures=False)

Clean-up the resources associated with the Executor.

It is safe to call this method several times. Otherwise, no other
methods can be called after this one.

Args:
: wait: If True then shutdown will not return until all running
  : futures have finished executing and the resources used by the
    executor have been reclaimed.
  <br/>
  cancel_futures: If True then shutdown will cancel all pending
  : futures. Futures that are completed or running will not be
    cancelled.

#### submit(fn, , \*args, \*\*kwargs)

Submits a callable to be executed with the given arguments.

Schedules the callable to be executed as fn(

```
*
```

args, 

```
**
```

kwargs) and returns
a Future instance representing the execution of the callable.

Returns:
: A Future representing the given call.

### *class* adaptivetesting.simulation.ResultOutputFormat(\*values)

Bases: `Enum`

Enum for selecting the output format for
the test results

#### CSV *= 1*

#### PICKLE *= 2*

### *class* adaptivetesting.simulation.Simulation(test: [AdaptiveTest](#adaptivetesting.simulation.AdaptiveTest), test_result_output: [ResultOutputFormat](#adaptivetesting.simulation.ResultOutputFormat))

Bases: `object`

This class can be used for simulating CAT.

Args:
: test (AdaptiveTest): instance of an adaptive test implementation (see implementations module)
  <br/>
  test_result_output (ResultOutputFormat): test results output format

#### save_test_results()

Saves the test results to the specified output format.

#### simulate(criterion: [StoppingCriterion](#adaptivetesting.simulation.StoppingCriterion) | list[[StoppingCriterion](#adaptivetesting.simulation.StoppingCriterion)] = StoppingCriterion.SE, value: float | list[float | int] = 0.4)

Runs the adaptive test simulation until the specified stopping criterion or criteria are met.

Args:
: criterion (StoppingCriterion | list[StoppingCriterion]):
  : The stopping criterion or list of criteria to determine when the test should stop.
    Supported values are StoppingCriterion.SE (standard error) and StoppingCriterion.LENGTH (test length).
  <br/>
  value (float | list[float | int]):
  : The threshold value(s) for the stopping criterion. For SE, this is the maximum allowed standard error.
    For LENGTH, this is the maximum number of items administered.

### *class* adaptivetesting.simulation.SimulationPool(adaptive_tests: list[[AdaptiveTest](#adaptivetesting.simulation.AdaptiveTest)], test_result_output: [ResultOutputFormat](#adaptivetesting.simulation.ResultOutputFormat), criterion: [StoppingCriterion](#adaptivetesting.simulation.StoppingCriterion) | list[[StoppingCriterion](#adaptivetesting.simulation.StoppingCriterion)] = StoppingCriterion.SE, value: float = 0.4)

Bases: `object`

A pool manager for running multiple adaptive test simulations in parallel.

Args:
: adaptive_tests (list[AdaptiveTest]): List of adaptive test instances to be simulated.
  <br/>
  test_results_output (ResultOutputFormat): Format for outputting test results.
  <br/>
  criterion (StoppingCriterion | list[StoppingCriterion]):
  : Stopping criterion or list of criteria for the simulations.
  <br/>
  value (float): Value associated with the stopping criterion (default is 0.4).

#### start()

Starts the simulation by executing adaptive tests in parallel.

Depending on the operating system, uses either multithreading (on Windows)
or multiprocessing (on other platforms) to run the simulation for each adaptive test.
Progress is displayed using a progress bar.

### *class* adaptivetesting.simulation.StoppingCriterion(\*values)

Bases: `Enum`

Enum for selecting the stopping criterion
for the adaptive test

#### LENGTH *= 2*

#### SE *= 1*

### *class* adaptivetesting.simulation.ThreadPoolExecutor(max_workers=None, thread_name_prefix='', initializer=None, initargs=())

Bases: `Executor`

Initializes a new ThreadPoolExecutor instance.

Args:
: max_workers: The maximum number of threads that can be used to
  : execute the given calls.
  <br/>
  thread_name_prefix: An optional name prefix to give our threads.
  initializer: A callable used to initialize worker threads.
  initargs: A tuple of arguments to pass to the initializer.

#### shutdown(wait=True, , cancel_futures=False)

Clean-up the resources associated with the Executor.

It is safe to call this method several times. Otherwise, no other
methods can be called after this one.

Args:
: wait: If True then shutdown will not return until all running
  : futures have finished executing and the resources used by the
    executor have been reclaimed.
  <br/>
  cancel_futures: If True then shutdown will cancel all pending
  : futures. Futures that are completed or running will not be
    cancelled.

#### submit(fn, , \*args, \*\*kwargs)

Submits a callable to be executed with the given arguments.

Schedules the callable to be executed as fn(

```
*
```

args, 

```
**
```

kwargs) and returns
a Future instance representing the execution of the callable.

Returns:
: A Future representing the given call.

### adaptivetesting.simulation.as_completed(fs, timeout=None)

An iterator over the given futures that yields each as it completes.

Args:
: fs: The sequence of Futures (possibly created by different Executors) to
  : iterate over.
  <br/>
  timeout: The maximum number of seconds to wait. If None, then there
  : is no limit on the wait time.

Returns:
: An iterator that yields the given Futures as they complete (finished or
  cancelled). If any given Futures are duplicated, they will be returned
  once.

Raises:
: TimeoutError: If the entire result iterator could not be generated
  : before the given timeout.

### *class* adaptivetesting.simulation.partial

Bases: `object`

partial(func, 

```
*
```

args, 

```
**
```

keywords) - new function with partial application
of the given arguments and keywords.

#### args

tuple of arguments to future partial calls

#### func

function object to use in future partial calls

#### keywords

dictionary of keyword arguments to future partial calls

### adaptivetesting.simulation.setup_simulation_and_start(test: [AdaptiveTest](#adaptivetesting.simulation.AdaptiveTest), test_result_output: [ResultOutputFormat](#adaptivetesting.simulation.ResultOutputFormat), criterion: [StoppingCriterion](#adaptivetesting.simulation.StoppingCriterion) | list[[StoppingCriterion](#adaptivetesting.simulation.StoppingCriterion)], value: float)

Sets up and runs a simulation for an adaptive test, then saves the results.

Args:
: test (AdaptiveTest): The adaptive test instance to be simulated.
  <br/>
  test_result_output (ResultOutputFormat): The format or handler for outputting test results.
  <br/>
  criterion (StoppingCriterion | list[StoppingCriterion]):
  : The criterion used to determine when the simulation should stop.
  <br/>
  value (float):
  : The value associated with the stopping criterion (e.g., maximum number of items, target standard error).

### *class* adaptivetesting.simulation.tqdm(\*\_, \*\*\_\_)

Bases: `Comparable`

Decorate an iterable object, returning an iterator which acts exactly
like the original iterable, but prints a dynamically updating
progressbar every time a value is requested.

## Parameters

iterable
: Iterable to decorate with a progressbar.
  Leave blank to manually manage the updates.

desc
: Prefix for the progressbar.

total
: The number of expected iterations. If unspecified,
  len(iterable) is used if possible. If float(“inf”) or as a last
  resort, only basic progress statistics are displayed
  (no ETA, no progressbar).
  If gui is True and this parameter needs subsequent updating,
  specify an initial arbitrary large positive number,
  e.g. 9e9.

leave
: If [default: True], keeps all traces of the progressbar
  upon termination of iteration.
  If None, will leave only if position is 0.

file
: Specifies where to output the progress messages
  (default: sys.stderr). Uses file.write(str) and file.flush()
  methods.  For encoding, see write_bytes.

ncols
: The width of the entire output message. If specified,
  dynamically resizes the progressbar to stay within this bound.
  If unspecified, attempts to use environment width. The
  fallback is a meter width of 10 and no limit for the counter and
  statistics. If 0, will not print any meter (only stats).

mininterval
: Minimum progress display update interval [default: 0.1] seconds.

maxinterval
: Maximum progress display update interval [default: 10] seconds.
  Automatically adjusts miniters to correspond to mininterval
  after long display update lag. Only works if dynamic_miniters
  or monitor thread is enabled.

miniters
: Minimum progress display update interval, in iterations.
  If 0 and dynamic_miniters, will automatically adjust to equal
  mininterval (more CPU efficient, good for tight loops).
  If > 0, will skip display of specified number of iterations.
  Tweak this and mininterval to get very efficient loops.
  If your progress is erratic with both fast and slow iterations
  (network, skipping items, etc) you should set miniters=1.

ascii
: If unspecified or False, use unicode (smooth blocks) to fill
  the meter. The fallback is to use ASCII characters “ 123456789#”.

disable
: Whether to disable the entire progressbar wrapper
  [default: False]. If set to None, disable on non-TTY.

unit
: String that will be used to define the unit of each iteration
  [default: it].

unit_scale
: If 1 or True, the number of iterations will be reduced/scaled
  automatically and a metric prefix following the
  International System of Units standard will be added
  (kilo, mega, etc.) [default: False]. If any other non-zero
  number, will scale total and n.

dynamic_ncols
: If set, constantly alters ncols and nrows to the
  environment (allowing for window resizes) [default: False].

smoothing
: Exponential moving average smoothing factor for speed estimates
  (ignored in GUI mode). Ranges from 0 (average speed) to 1
  (current/instantaneous speed) [default: 0.3].

bar_format
: Specify a custom bar string formatting. May impact performance.
  [default: ‘{l_bar}{bar}{r_bar}’], where
  l_bar=’{desc}: {percentage:3.0f}%|’ and
  r_bar=’| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, ‘
  <br/>
  > ‘{rate_fmt}{postfix}]’
  <br/>
  Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
  : percentage, elapsed, elapsed_s, ncols, nrows, desc, unit,
    rate, rate_fmt, rate_noinv, rate_noinv_fmt,
    rate_inv, rate_inv_fmt, postfix, unit_divisor,
    remaining, remaining_s, eta.
  <br/>
  Note that a trailing “: “ is automatically removed after {desc}
  if the latter is empty.

initial
: The initial counter value. Useful when restarting a progress
  bar [default: 0]. If using float, consider specifying {n:.3f}
  or similar in bar_format, or specifying unit_scale.

position
: Specify the line offset to print this bar (starting from 0)
  Automatic if unspecified.
  Useful to manage multiple bars at once (eg, from threads).

postfix
: Specify additional stats to display at the end of the bar.
  Calls set_postfix(\*\*postfix) if possible (dict).

unit_divisor
: [default: 1000], ignored unless unit_scale is True.

write_bytes
: Whether to write bytes. If (default: False) will write unicode.

lock_args
: Passed to refresh for intermediate output
  (initialisation, iterating, and updating).

nrows
: The screen height. If specified, hides nested bars outside this
  bound. If unspecified, attempts to use environment height.
  The fallback is 20.

colour
: Bar colour (e.g. ‘green’, ‘#00ff00’).

delay
: Don’t display until [default: 0] seconds have elapsed.

gui
: WARNING: internal parameter - do not use.
  Use tqdm.gui.tqdm(…) instead. If set, will attempt to use
  matplotlib animations for a graphical output [default: False].

## Returns

out  : decorated iterator.

#### clear(nolock=False)

Clear current bar display.

#### close()

Cleanup and (if leave=False) close the progressbar.

#### display(msg=None, pos=None)

Use self.sp to display msg in the specified pos.

Consider overloading this function when inheriting to use e.g.:
self.some_frontend(\*\*self.format_dict) instead of self.sp.

### Parameters

msg  : str, optional. What to display (default: repr(self)).
pos  : int, optional. Position to moveto

> (default: abs(self.pos)).

#### *classmethod* external_write_mode(file=None, nolock=False)

Disable tqdm within context and refresh tqdm when exits.
Useful when writing to standard output stream

#### *property* format_dict

Public API for read-only member access.

#### *static* format_interval(t)

Formats a number of seconds as a clock time, [H:]MM:SS

### Parameters

t
: Number of seconds.

### Returns

out
: [H:]MM:SS

#### *static* format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False, unit='it', unit_scale=False, rate=None, bar_format=None, postfix=None, unit_divisor=1000, initial=0, colour=None, \*\*extra_kwargs)

Return a string-based progress bar given some parameters

### Parameters

n
: Number of finished iterations.

total
: The expected total number of iterations. If meaningless (None),
  only basic progress statistics are displayed (no ETA).

elapsed
: Number of seconds passed since start.

ncols
: The width of the entire output message. If specified,
  dynamically resizes {bar} to stay within this bound
  [default: None]. If 0, will not print any bar (only stats).
  The fallback is {bar:10}.

prefix
: Prefix message (included in total width) [default: ‘’].
  Use as {desc} in bar_format string.

ascii
: If not set, use unicode (smooth blocks) to fill the meter
  [default: False]. The fallback is to use ASCII characters
  “ 123456789#”.

unit
: The iteration unit [default: ‘it’].

unit_scale
: If 1 or True, the number of iterations will be printed with an
  appropriate SI metric prefix (k = 10^3, M = 10^6, etc.)
  [default: False]. If any other non-zero number, will scale
  total and n.

rate
: Manual override for iteration rate.
  If [default: None], uses n/elapsed.

bar_format
: Specify a custom bar string formatting. May impact performance.
  [default: ‘{l_bar}{bar}{r_bar}’], where
  l_bar=’{desc}: {percentage:3.0f}%|’ and
  r_bar=’| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, ‘
  <br/>
  > ‘{rate_fmt}{postfix}]’
  <br/>
  Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
  : percentage, elapsed, elapsed_s, ncols, nrows, desc, unit,
    rate, rate_fmt, rate_noinv, rate_noinv_fmt,
    rate_inv, rate_inv_fmt, postfix, unit_divisor,
    remaining, remaining_s, eta.
  <br/>
  Note that a trailing “: “ is automatically removed after {desc}
  if the latter is empty.

postfix
: Similar to prefix, but placed at the end
  (e.g. for additional stats).
  Note: postfix is usually a string (not a dict) for this method,
  and will if possible be set to postfix = ‘, ‘ + postfix.
  However other types are supported (#382).

unit_divisor
: [default: 1000], ignored unless unit_scale is True.

initial
: The initial counter value [default: 0].

colour
: Bar colour (e.g. ‘green’, ‘#00ff00’).

### Returns

out  : Formatted meter and stats, ready to display.

#### *static* format_num(n)

Intelligent scientific notation (.3g).

### Parameters

n
: A Number.

### Returns

out
: Formatted number.

#### *static* format_sizeof(num, suffix='', divisor=1000)

Formats a number (greater than unity) with SI Order of Magnitude
prefixes.

### Parameters

num
: Number ( >= 1) to format.

suffix
: Post-postfix [default: ‘’].

divisor
: Divisor between prefixes [default: 1000].

### Returns

out
: Number with Order of Magnitude SI unit postfix.

#### *classmethod* get_lock()

Get the global lock. Construct it if it does not exist.

#### monitor *= None*

#### monitor_interval *= 10*

#### moveto(n)

#### *classmethod* pandas(\*\*tqdm_kwargs)

Registers the current tqdm class with
: pandas.core.
  ( frame.DataFrame
  | series.Series
  | groupby.(generic.)DataFrameGroupBy
  | groupby.(generic.)SeriesGroupBy
  ).progress_apply

A new instance will be created every time progress_apply is called,
and each instance will automatically close() upon completion.

### Parameters

tqdm_kwargs  : arguments for the tqdm instance

### Examples

```pycon
>>> import pandas as pd
>>> import numpy as np
>>> from tqdm import tqdm
>>> from tqdm.gui import tqdm as tqdm_gui
>>>
>>> df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))
>>> tqdm.pandas(ncols=50)  # can use tqdm_gui, optional kwargs, etc
>>> # Now you can use `progress_apply` instead of `apply`
>>> df.groupby(0).progress_apply(lambda x: x**2)
```

### References

<[https://stackoverflow.com/questions/18603270/](https://stackoverflow.com/questions/18603270/)        progress-indicator-during-pandas-operations-python>

#### refresh(nolock=False, lock_args=None)

Force refresh the display of this bar.

### Parameters

nolock
: If True, does not lock.
  If [default: False]: calls acquire() on internal lock.

lock_args
: Passed to internal lock’s acquire().
  If specified, will only display() if acquire() returns True.

#### reset(total=None)

Resets to 0 iterations for repeated use.

Consider combining with leave=True.

### Parameters

total  : int or float, optional. Total to use for the new bar.

#### set_description(desc=None, refresh=True)

Set/modify description of the progress bar.

### Parameters

desc  : str, optional
refresh  : bool, optional

> Forces refresh [default: True].

#### set_description_str(desc=None, refresh=True)

Set/modify description without ‘: ‘ appended.

#### *classmethod* set_lock(lock)

Set the global lock.

#### set_postfix(ordered_dict=None, refresh=True, \*\*kwargs)

Set/modify postfix (additional stats)
with automatic formatting based on datatype.

### Parameters

ordered_dict  : dict or OrderedDict, optional
refresh  : bool, optional

> Forces refresh [default: True].

kwargs  : dict, optional

#### set_postfix_str(s='', refresh=True)

Postfix without dictionary expansion, similar to prefix handling.

#### *static* status_printer(file)

Manage the printing and in-place updating of a line of characters.
Note that if the string is longer than a line, then in-place
updating may not work (it will print a new line at each refresh).

#### unpause()

Restart tqdm timer from last print time.

#### update(n=1)

Manually update the progress bar, useful for streams
such as reading files.
E.g.:
>>> t = tqdm(total=filesize) # Initialise
>>> for current_buffer in stream:
…    …
…    t.update(len(current_buffer))
>>> t.close()
The last line is highly recommended, but possibly not necessary if
t.update() will be called in such a way that filesize will be
exactly reached and printed.

### Parameters

n
: Increment to add to the internal counter of iterations
  [default: 1]. If using float, consider specifying {n:.3f}
  or similar in bar_format, or specifying unit_scale.

### Returns

out
: True if a display() was triggered.

#### *classmethod* wrapattr(stream, method, total=None, bytes=True, \*\*tqdm_kwargs)

stream  : file-like object.
method  : str, “read” or “write”. The result of read() and

> the first argument of write() should have a len().
```pycon
>>> with tqdm.wrapattr(file_obj, "read", total=file_obj.size) as fobj:
...     while True:
...         chunk = fobj.read(chunk_size)
...         if not chunk:
...             break
```

#### *classmethod* write(s, file=None, end='\\n', nolock=False)

Print a message via tqdm (without overlap with bars).
