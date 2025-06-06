import unittest
from adaptivetesting.simulation.__simulation import SimulationPool, ResultOutputFormat, StoppingCriterion

class DummyItemPool:
    def __init__(self, n_items):
        self.test_items = list(range(n_items))

class DummyTestResult:
    def __init__(self, test_id, ability_estimation=0.0, standard_error=0.0):
        self.test_id = test_id
        self.ability_estimation = ability_estimation
        self.standard_error = standard_error
        self.showed_item = "H"
        self.response = 0
        self.true_ability_level = float("NaN")

class DummyAdaptiveTest:
    def __init__(self, n_items=1, simulation_id=0, participant_id=0):
        self.item_pool = DummyItemPool(n_items)
        self.test_results = []
        self.simulation_id = simulation_id
        self.participant_id = participant_id
        self._run_count = 0

    def run_test_once(self):
        # Simulate answering one item per run
        if self.item_pool.test_items:
            self.item_pool.test_items.pop()
            self._run_count += 1
            # Append a DummyTestResult instead of a string
            self.test_results.append(DummyTestResult(
                test_id=f"{self.simulation_id}_{self.participant_id}_{self._run_count}",
                ability_estimation=float(self._run_count),
                standard_error=0.1 * self._run_count
            ))

    def check_se_criterion(self, value):
        return not self.item_pool.test_items

    def check_length_criterion(self, value):
        return not self.item_pool.test_items

class TestSimulationPoolIntegration(unittest.TestCase):
    def test_simulation_pool_with_real_data(self):
        tests = [DummyAdaptiveTest(n_items=2, simulation_id=i, participant_id=100+i) for i in range(3)]
        pool = SimulationPool(
            adaptive_tests=tests,
            test_result_output=ResultOutputFormat.PICKLE,
            criterion=StoppingCriterion.SE,
            value=0.4
        )
        import adaptivetesting.simulation.__simulation as sim_mod
        orig_pool = sim_mod.Pool
        sim_mod.Pool = lambda n: type('FakePool', (), {
            '__enter__': lambda self: self,
            '__exit__': lambda self, exc_type, exc_val, exc_tb: None,
            'map': lambda self, func, iterable: [func(test) for test in iterable]
        })()
        try:
            pool.start()
            for test in tests:
                self.assertEqual(len(test.test_results), 2)
                # Check that results are DummyTestResult instances
                self.assertTrue(all(isinstance(r, DummyTestResult) for r in test.test_results))
        finally:
            sim_mod.Pool = orig_pool

    def test_simulation_pool_with_real_data_sqlite(self):
        tests = [DummyAdaptiveTest(n_items=2, simulation_id=i, participant_id=100+i) for i in range(3)]
        pool = SimulationPool(
            adaptive_tests=tests,
            test_result_output=ResultOutputFormat.SQLITE,
            criterion=StoppingCriterion.SE,
            value=0.4
        )
        import adaptivetesting.simulation.__simulation as sim_mod
        orig_pool = sim_mod.Pool
        sim_mod.Pool = lambda n: type('FakePool', (), {
            '__enter__': lambda self: self,
            '__exit__': lambda self, exc_type, exc_val, exc_tb: None,
            'map': lambda self, func, iterable: [func(test) for test in iterable]
        })()
        try:
            pool.start()
            for test in tests:
                self.assertEqual(len(test.test_results), 2)
                self.assertTrue(all(isinstance(r, DummyTestResult) for r in test.test_results))
        finally:
            sim_mod.Pool = orig_pool

if __name__ == '__main__':
    unittest.main()