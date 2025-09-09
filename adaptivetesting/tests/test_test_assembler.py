import unittest
from unittest.mock import patch
from adaptivetesting.implementations.__test_assembler import TestAssembler
from adaptivetesting.models.__algorithm_exception import AlgorithmException
from adaptivetesting.models import TestItem, ItemPool
from adaptivetesting.services import IEstimator


# Dummy classes for dependencies
class DummyTestItem(TestItem):
    def __init__(self, id=0):
        self.id = id
    
    def as_dict(self, with_id: bool = True) -> dict[str, float | int | None]:
        return {"id": self.id}


class DummyItemPool(ItemPool):
    
    def __init__(self, items=None):
        self.test_items = items or [DummyTestItem(i) for i in range(3)]
        self.deleted = []
        self.simulated_responses = []
    
    def get_item_response(self, item):
        return 1 if item.id % 2 == 0 else 0
    
    def delete_item(self, item):
        self.deleted.append(item)
        self.test_items = [i for i in self.test_items if i.id != item.id]


class DummyEstimator(IEstimator):
    def __init__(self, response_pattern, answered_items, **kwargs):
        self.response_pattern = response_pattern
        self.answered_items = answered_items
        self.kwargs = kwargs
    
    def get_estimation(self):
        if hasattr(self, "raise_exception") and self.raise_exception:
            raise AlgorithmException("Estimation failed")
        return 5.0
    
    def get_standard_error(self, estimation):
        return 0.5


def dummy_item_selector(items, ability, **kwargs):
    return items[0]


class TestTestAssembler(unittest.TestCase):

    def setUp(self):
        self.assembler = TestAssembler(
            item_pool=DummyItemPool(),
            simulation_id="sim1",
            participant_id="p1",
            ability_estimator=DummyEstimator,
            estimator_args={},
            item_selector=dummy_item_selector,
            item_selector_args={},
            pretest=False,
            simulation=True,
            debug=False
        )

    def test_init_sets_attributes(self):
        assembler = TestAssembler(
            item_pool=DummyItemPool(),
            simulation_id="sim1",
            participant_id="p1",
            ability_estimator=DummyEstimator,
            estimator_args={"foo": "bar"},
            item_selector=dummy_item_selector,
            item_selector_args={"baz": 1},
            pretest=True,
            pretest_seed=123,
            simulation=True,
            debug=True
        )
        self.assertEqual(assembler._TestAssembler__ability_estimator, DummyEstimator) # type: ignore
        self.assertEqual(assembler._TestAssembler__estimator_args, {"foo": "bar"}) # type: ignore
        self.assertEqual(assembler._TestAssembler__item_selector, dummy_item_selector) # type: ignore
        self.assertEqual(assembler._TestAssembler__item_selector_args, {"baz": 1}) # type: ignore
        self.assertTrue(assembler._TestAssembler__pretest) # type: ignore
        self.assertEqual(assembler._TestAssembler__pretest_seed, 123) # type: ignore

    def test_estimate_ability_level_normal_case(self):
        self.assembler.response_pattern = [1, 0, 1]
        self.assembler.answered_items = [DummyTestItem(1), DummyTestItem(2), DummyTestItem(3)]
        est, se = self.assembler.estimate_ability_level()
        self.assertEqual(est, 5.0)
        self.assertEqual(se, 0.5)

    def test_estimate_ability_level_all_correct(self):
        assembler = TestAssembler(
            item_pool=DummyItemPool(),
            simulation_id="sim1",
            participant_id="p1",
            ability_estimator=DummyEstimator,
            estimator_args={},
            item_selector=dummy_item_selector,
            item_selector_args={},
            pretest=False,
            simulation=True,
            debug=False
        )
        assembler.response_pattern = [1, 1, 1]
        assembler.answered_items = [DummyTestItem(1), DummyTestItem(2), DummyTestItem(3)]
        with patch.object(DummyEstimator, "get_estimation", side_effect=AlgorithmException("fail")), \
             patch.object(DummyEstimator, "get_standard_error", return_value=0.5):
            est, se = assembler.estimate_ability_level()
            self.assertEqual(est, 10)
            self.assertEqual(se, 0.5)

    def test_estimate_ability_level_all_incorrect(self):
        assembler = TestAssembler(
            item_pool=DummyItemPool(),
            simulation_id="sim1",
            participant_id="p1",
            ability_estimator=DummyEstimator,
            estimator_args={},
            item_selector=dummy_item_selector,
            item_selector_args={},
            pretest=False,
            simulation=True,
            debug=False
        )
        assembler.response_pattern = [0, 0, 0]
        assembler.answered_items = [DummyTestItem(1), DummyTestItem(2), DummyTestItem(3)]
        with patch.object(DummyEstimator, "get_estimation", side_effect=AlgorithmException("fail")), \
             patch.object(DummyEstimator, "get_standard_error", return_value=0.5):
            est, se = assembler.estimate_ability_level()
            self.assertEqual(est, -10)
            self.assertEqual(se, 0.5)

    def test_estimate_ability_level_raises_on_other_exception(self):
        assembler = TestAssembler(
            item_pool=DummyItemPool(),
            simulation_id="sim1",
            participant_id="p1",
            ability_estimator=DummyEstimator,
            estimator_args={},
            item_selector=dummy_item_selector,
            item_selector_args={},
            pretest=False,
            simulation=True,
            debug=False
        )
        assembler.response_pattern = [1, 0, 0]
        assembler.answered_items = [DummyTestItem(1), DummyTestItem(2), DummyTestItem(3)]
        with patch.object(DummyEstimator, "get_estimation", side_effect=AlgorithmException("fail")):
            with self.assertRaises(AlgorithmException):
                assembler.estimate_ability_level()

    def test_get_next_item_calls_selector(self):
        self.assembler.ability_level = 1.5
        item = self.assembler.get_next_item()
        self.assertIsInstance(item, DummyTestItem)
        self.assertEqual(item.id, 0)

    def test_run_test_once_calls_super(self):
        dummy_items = [DummyTestItem(i) for i in range(2)]
        dummy_pool = DummyItemPool(items=dummy_items.copy())
        assembler = TestAssembler(
            item_pool=dummy_pool,
            simulation_id="sim1",
            participant_id="p1",
            ability_estimator=DummyEstimator,
            estimator_args={},
            item_selector=dummy_item_selector,
            item_selector_args={},
            pretest=True,
            pretest_seed=42,
            simulation=True,
            debug=False
        )
        assembler.response_pattern = []
        assembler.answered_items = []
        assembler.test_results = []
        assembler.simulation = True

        class DummyPreTest:
            def __init__(self, items, seed):
                self.items = items
                self.seed = seed
            
            def select_random_item_quantile(self):
                return self.items

        class DummyTestResult:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        with patch("adaptivetesting.implementations.__test_assembler.PreTest", DummyPreTest), \
             patch("adaptivetesting.implementations.__test_assembler.TestResult", DummyTestResult), \
             patch("adaptivetesting.models.__adaptive_test.AdaptiveTest.run_test_once",
                   autospec=True) as dummy_super_run:
            dummy_super_run.return_value = "done"
            result = assembler.run_test_once()
            self.assertEqual(result, "done")
            self.assertTrue(dummy_super_run.called)
            self.assertEqual(len(assembler.test_results), len(dummy_items))
