import unittest
from unittest.mock import patch

from adaptivetesting.math.exposure_control.__mpi_exposure_control import (
    MaximumPriorityIndexExposureControl,
)
from adaptivetesting import ResultOutputFormat, Constraint


class DummyConstraint:
    def __init__(self, name, weight=1.0, prevalence=0.0):
        self.name = name
        self.weight = weight
        self.prevalence = prevalence


class DummyItem:
    def __init__(self, identifier, categories):
        # production code expects item.additional_properties["category"]
        self.identifier = identifier
        self.additional_properties = {"category": categories}


class DummyItemPool:
    def __init__(self, items):
        self.test_items = items


class DummyAdaptiveTest:
    def __init__(self, items, simulation_id="sim1", ability_level=0.0):
        self.item_pool = DummyItemPool(items)
        self.simulation_id = simulation_id
        self.ability_level = ability_level


class MPIExposureControlTests(unittest.TestCase):
    @patch(
        "adaptivetesting.math.exposure_control.__mpi_exposure_control.read_prev_items",
        return_value=[],
    )
    @patch(
        "adaptivetesting.math.exposure_control.__mpi_exposure_control.compute_priority_index"
    )
    def test_selects_item_with_highest_priority_index(self, mock_compute, _mock_read):
        # arrange: three items with different categories
        i1 = DummyItem("i1", ["A"])
        i2 = DummyItem("i2", ["B"])
        i3 = DummyItem("i3", ["A"])
        adaptive = DummyAdaptiveTest([i1, i2, i3])

        constraints = [
            DummyConstraint("A", weight=1.0, prevalence=2.0),
            DummyConstraint("B", weight=1.0, prevalence=1.0),
        ]

        scores = {"i1": 0.2, "i2": 0.8, "i3": 0.5}

        def fake_compute(item, **kwargs):
            res = scores.get(str(getattr(item, "identifier", None)), 0.0)
            return res

        mock_compute.side_effect = fake_compute

        controller = MaximumPriorityIndexExposureControl(
            adaptive, constraints, participant_ids=["p1"],
            format=ResultOutputFormat.CSV
        )
        selected = controller.select_item()

        self.assertIs(selected, i2)  # item with score 0.8 should be chosen

    @patch(
        "adaptivetesting.math.exposure_control.__mpi_exposure_control.read_prev_items",
        return_value=[],
    )
    def test_returns_none_on_empty_pool(self, _mock_read):
        adaptive = DummyAdaptiveTest([])
        constraints: list[Constraint] = []
        controller = MaximumPriorityIndexExposureControl(adaptive,
                                                         constraints,
                                                         participant_ids=[],
                                                         format=ResultOutputFormat.CSV)
        self.assertIsNone(controller.select_item())


if __name__ == "__main__":
    unittest.main()
