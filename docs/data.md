# data Module

## PickleContext

### *class* adaptivetesting.data.PickleContext(simulation_id: str, participant_id: int)

Bases: [`ITestResults`](services.md#adaptivetesting.services.ITestResults)

Implementation of the ITestResults interface for
saving test results to the pickle format.
The resulting pickle file <simulation_id>.pickle
will be of the standard pickle format which depends
on the used python version.

Args:
: simulation_id (str): Not used but required by the interface
  <br/>
  participant_id (int): participant id and table name

#### load() → List[[TestResult](models.md#adaptivetesting.models.TestResult)]

Loads results from the database.
The implementation of this method is required
by the interface. However, is does not have
any implemented functionality and will throw an error
if used.

Returns: List[TestResult]

#### save(test_results: List[[TestResult](models.md#adaptivetesting.models.TestResult)]) → None

Saves a list of test results to a pickle binary file
(<participant_id>.pickle).

Args:
: test_results (List[TestResult]): list of test results

## SQLiteContext

### *class* adaptivetesting.data.SQLiteContext(simulation_id: str, participant_id: int)

Bases: [`ITestResults`](services.md#adaptivetesting.services.ITestResults)

Implementation of the ITestResults interface for
saving test results to a SQLITE database.
The resulting sqlite file <simulation_id>.db
will be of the SQLITE3 format.

Args:
: simulation_id (str): db filename
  <br/>
  participant_id (int): participant id and table name

#### load() → List[[TestResult](models.md#adaptivetesting.models.TestResult)]

Loads results from the database.
The implementation of this method is required
by the interface. However, is does not have
any implemented functionality and will throw an error.

Returns: List[TestResult]

#### save(test_results: List[[TestResult](models.md#adaptivetesting.models.TestResult)]) → None

Saves a list of test results to the database
in the table <participant_id>.

Args:
: test_results (List[TestResult]): list of test results
