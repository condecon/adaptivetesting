# Content Balancing
This package currently supports two methods for Content Balancing:
- Maximum Priority Index (Cheng & Chang, 2009)
- Weighted Penalty Model (Shin et al., 2009)

## Maximum Priority Index
n MPI, items are assigned to groups. These groups, in turn, belong to constraints. 
These constraints are implemented in the package as follows:
- Constraint name (important for the correct assignment of items)
- Weight
- Prevalence (Frequency / Relative Frequency of a constraint and its items)
For more background information, please refer to Cheng & Chang (2009).

### Setup Item Pool
It is important to note that each item in the item pool 
must be assigned to one or more content categories. 
These specify which constraints the item is relevant to. 
Therefore of course, an item can belong to multiple constraints.

````python
import adaptivetesting as adt
import pandas as pd

items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1],
            "content_categories": ["Math", "English", "Math"],
            "id": [1, 2, 3]
        })
````
In this example, we have two items belonging to the content category `Math` and one
to `English`.

### Setup Adaptive Test
The adaptive test can, in general, be set up as usual.
But some additional properties, i.e. the constraints, have to be defined.
For simplicity, we will define all the arguments required for Content Balancing
prior to the test object.
```python
cb_args: adt.ContentBalancingArgs = {
            "constraints": [
                adt.Constraint("Math", weight=0.5, prevalence=0.5),
                adt.Constraint("English", weight=0.5, prevalence=0.5)
            ]
        }
```
In this example, we set the prevalence and the weight of both constraints to `0.5`.
The test can then be assembled.
```python
adaptive_test = adt.TestAssembler(
            item_pool=item_pool,
            simulation_id="1",
            participant_id="2",
            ability_estimator=adt.MLEstimator,
            content_balancing="MaximumPriorityIndex",
            content_balancing_args=cb_args
        )
```

## Weighted Penalty Model
The WPM itself follows a very complex ruleset. 
For more background on the operation of the WPM, see Shin et al. (2009).

To implement the WPM in an adaptive test, constraints have to be defined.
These consist of the following properties:
- name
- weight
- prevalence (0 < x < 1)
- lower bound
- upper bound

Again, we will define all the arguments required for Content Balancing
before the actual test object.
```python
cb_args: adt.ContentBalancingArgs = {
    "constraints": [
                    adt.Constraint(
                        "Math",
                        weight=0.5,
                        prevalence=0.2,
                        lower=0,
                        upper=1
                    ),
                    adt.Constraint(
                        "English",
                        weight=0.5,
                        prevalence=0.2,
                        lower=0,
                        upper=1
                    )
                ],
                "constraint_weight": 0.5,
                "information_weight": 0.5
}
```
WEP also requires to weight the constraints and item information.
In this example, the weights are fixed but can also be set to functions so that
the weights may be adapted during the testing procedure.
For that, `"constraint_weight"` and/or `"information_weight"` must be set to
functions that take an instance of the adaptive test as argument 
and return a float (`Callable[[AdaptiveTest], float]`).

Finally, the adaptive test can be specified as usual.
```python
adaptive_test = adt.TestAssembler(
            item_pool=item_pool,
            simulation_id="1",
            participant_id="12",
            ability_estimator=adt.MLEstimator,
            content_balancing="WeightedPenaltyModel",
            content_balancing_args=cb_args
        )
```

## References
Cheng, Y., & Chang, H. (2009). The maximum priority index method for severely constrained item selection
in computerized adaptive testing.
British Journal of Mathematical and Statistical Psychology, 62(2), 369–383.
https://doi.org/10.1348/000711008X304376

Shin, C. D., Chien, Y., Way, W. D., & Swanson, L. (2009, April). Weighted Penalty
Model for Content Balancing in CATS.
https://www.pearsonassessments.com/content/dam/school/global/clinical/us/
assets/testnav/weighted-penalty-model.pdf