# Testing Software
With `adaptivetesting`, users can simulate adaptive tests
but also collect real data.
For data collection, a function has to be defined
which allows interaction with the examinees.
This can be via testing software such as PsychoPy or any 
other appropriate interface.

In this example, we will just collect responses from the commandline.
In real-world data collection, items selected from the test can be used to match the appropriate stimuli
which are then displayed to the participants.
```python
import adaptivetesting as adt

def get_response (item : adt.TestItem) -> int:
    print(f"Selected item: {item.id}")
    response = input("Response >")
    return int(response)
```

Then, we can set up the adaptive test object.
```python
adaptive_test = adt.TestAssembler (
    item_pool=item_pool,
    simulation_id="example_data_collection",
    participant_id="dummy",
    ability_estimator=adt.MLEstimator,
    item_selector=adt.maximum_information_criterion,
    simulation=False
    )
```
It is important that the `simulation` parameter is set to `False` so that the package
does not simulate responses but expects real user input.
To enable data collection, the `get_response` method of the 
test object has to be overridden.
```python
adaptive_test.get_response = get_response
```

Simple additional code is required to let the test run until a stopping criterion is met
and the test results may be saved.
```python
# start adaptive test
while True:
    adaptive_test.run_test_once()

    # check stopping criterion
    if adaptive_test.standard_error <= 0.4:
        break

    # end test if all items have been shown
    if len(adaptive_test.item_pool.test_items) == 0:
        break

data_context = adt.CSVContext(
    adaptive_test.simulation_id,
    adaptive_test.participant_id
)

data_context.save(adaptive_test.test_results)
```