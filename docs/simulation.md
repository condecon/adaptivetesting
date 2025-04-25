# simulation Module

## ResultOutputFormat

### *class* adaptivetesting.simulation.ResultOutputFormat(\*values)

Bases: `Enum`

Enum for selecting the output format for
the test results

#### PICKLE *= 2*

#### SQLITE *= 1*

## StoppingCriterion

### *class* adaptivetesting.simulation.StoppingCriterion(\*values)

Bases: `Enum`

Enum for selecting the stopping criterion
for the adaptive test

#### LENGTH *= 2*

#### SE *= 1*

## Simulation

### *class* adaptivetesting.simulation.Simulation(test: [AdaptiveTest](models.md#adaptivetesting.models.AdaptiveTest), test_result_output: [ResultOutputFormat](#adaptivetesting.simulation.ResultOutputFormat))

Bases: `object`

This class can be used for simulating CAT.

Args:
: test (AdaptiveTest): instance of an adaptive test implementation (see implementations module)
  <br/>
  test_result_output (ResultOutputFormat): test results output format

#### save_test_results()

Saves the test results to the specified output format.

#### simulate(criterion: [StoppingCriterion](#adaptivetesting.simulation.StoppingCriterion) = StoppingCriterion.SE, value: float = 0.4)

Runs test until the stopping criterion is met.

Args:
: criterion (StoppingCriterion): selected stopping criterion
  <br/>
  value (float): either standard error value or test length value that has to be met by the test
