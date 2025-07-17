# data Module

### *class* adaptivetesting.data.CSVContext(simulation_id: str, participant_id: str)

Bases: [`ITestResults`](adaptivetesting.services.md#adaptivetesting.services.ITestResults)

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

### *class* adaptivetesting.data.PickleContext(simulation_id: str, participant_id: str)

Bases: [`ITestResults`](adaptivetesting.services.md#adaptivetesting.services.ITestResults)

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
