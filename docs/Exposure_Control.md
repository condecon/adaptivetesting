# Exposure Control

This package currently supports two methods for Exposure Control:
- Randomesque Item Selection (Kingsbury & Zara, 1989, 1991)
- Maximum Priority Index (Cheng & Chang, 2009)

## Randomesque 
Randomesque item selection does not select the *most* informative item,
instead a random draw is made from the $n$ most informative items. 
This can be easily set up in the `TestAssembler` by specifying
the `exposure_control` argument.
`exposure_control_args` takes a dictionary in which we can define the number
items and, if required, a seed for the random draw.

```python
import adaptivetesting as adt

test = adt.TestAssembler(
    ...,
    exposure_control="Randomesque",
    exposure_control_args={
        "n_items": 4,
        "seed": None
    }
)
```
The final test can then be used and run as usual.

## Maximum Priority Index
In MPI, items are assigned to groups. These groups, in turn, belong to constraints. 
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
For simplicity, we will define all the arguments required for Exposure Control
prior to the test object.
```python
ex_args: adt.ExposureControlArgs = {
            "constraints": [
                adt.Constraint("Math", weight=0.5, prevalence=0.5),
                adt.Constraint("English", weight=0.5, prevalence=0.5)
            ],
            "participant_ids": ["1"],
            "output_format": adt.ResultOutputFormat.CSV
        }
```
In this example, we set the prevalence and the weight of both constraints to `0.5`.
Additionally, we expect to have a single previous test results (from participant `"1"`) 
saved in the CSV file format.

The test can then be assembled.
```python
adaptive_test = adt.TestAssembler(
            item_pool=item_pool,
            simulation_id="1",
            participant_id="2",
            ability_estimator=adt.MLEstimator,
            exposure_control="MaximumPriorityIndex",
            exposure_control_args=ex_args,
            debug=False
        )
```

## References

Cheng, Y., & Chang, H. (2009). The maximum priority index method for severely constrained item selection
in computerized adaptive testing.
British Journal of Mathematical and Statistical Psychology, 62(2), 369–383.
https://doi.org/10.1348/000711008X304376

Kingsbury, G. G., & Zara, A. R. (1991). A Comparison of Procedures for Content-Sensitive
Item Selection in Computerized Adaptive Tests. Applied Measurement in Education, 4(3), 241–261.
Psychology and Behavioral Sciences Collection. https://doi.org/10.1207/s15324818ame0403_4

Kingsbury, G. G., & Zara, A. R. (1989). Procedures for selecting items for
computerized adaptive tests. Applied Measurement in Education, 2(4), 359–375.