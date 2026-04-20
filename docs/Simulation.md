# Simulation

## Single Simulation

For simulating an adaptive test, first the item pool has to be initialized.
```python
import adaptivetesting as adt
item_pool = adt.ItemPool.load_from_list(
    a = [0.42, 0.3, 1.5],
    b = [0.5, 0.9, 1.1]
)
```
Then, the test object can be created using the `TestAssembler` class. For reproducibility, a seed can be set.
```python
test = adt.TestAssembler(
    item_pool = item_pool,
    simulation_id="test",
    participant_id="1",
    ability_estimator=adt.MLEstimator,
    true_ability_level=0,
    seed=123
)
```

The simulation itself is set up with the `Simulation` class which specifies the output format for
the test results and the stopping criteria.
```python
simulation = adt.Simulation(test, adt.ResultOutputFormat.CSV)

simulation.simulate(criterion=adt.StoppingCriterion.SE, value=0.4)
simulation.save_test_results()
```

## Simulation Pool
For large scale simulations, the `SimulationPool` class can be used.
For every single simulation, a test object has to be created which needs to be saved in a list.
```python
tests = [
	adt.TestAssembler(
		item_pool=item_pool,
		simulation_id="example",
		participant_id="1",
		ability_estimator=adt.MLEstimator,
		item_selector=adt.maximum_information_criterion,
		true_ability_level=0,
		seed=123
	),
    adt.TestAssembler(
		item_pool=item_pool,
		simulation_id="example",
		participant_id="2",
		ability_estimator=adt.MLEstimator,
		item_selector=adt.maximum_information_criterion,
		true_ability_level=1,
		seed=123
	),
]
```
The simulation pool allows the tests to run sequentially without additional setup but also in parallel.
```python
sim_pool = adt.SimulationPool(
	adaptive_tests=tests,
	test_result_output=adt.ResultOutputFormat.CSV,
	criterion=adt.StoppingCriterion.SE,
	value=0.4
)
sim_pool.start()
```
Depending on the operating system, the simulation pool uses either multithreading (on Windows) 
or multiprocessing (on other platforms) to run the simulation for each adaptive test.
Note that parallel processing is not supported for the use in jupyter notebooks. 
For that, `parallel` has to be set to `False`.