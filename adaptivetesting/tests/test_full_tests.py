# This file is used to perform a full run of
# specific adaptiv test specifications.
import unittest
import adaptivetesting as adt
import pandas as pd
import shutil
import os
import pathlib


class TestContentBalancing(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)

        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1],
            "id": [1, 2, 3]
        })

        self.available_items = adt.ItemPool.load_from_dataframe(items).test_items
        self.content_categories = ["Math", "English", "Math"]

        for i, _ in enumerate(self.available_items):
            self.available_items[i].additional_properties = {
                "category": [self.content_categories[i]]
            }
        
    def test_maximum_priority_index(self):
        item_pool = adt.ItemPool(self.available_items, 
                                 [0, 1, 0])
        

        adaptive_test = adt.TestAssembler(
            item_pool=item_pool,
            simulation_id="1",
            participant_id="12",
            ability_estimator=adt.MLEstimator,
            content_balancing="MaximumPriorityIndex",
            content_balancing_args={
                "constraints": [
                    adt.Constraint(
                        "Math",
                        0.5,
                        0.2
                    ),
                    adt.Constraint(
                        "English",
                        0.5,
                        0.1
                    )
                ]
            }
        )

        sim = adt.Simulation(adaptive_test, adt.ResultOutputFormat.CSV)
        sim.simulate()

    def test_weighted_penalty_model(self):
        item_pool = adt.ItemPool(self.available_items, 
                                 [0, 1, 0])
        

        adaptive_test = adt.TestAssembler(
            item_pool=item_pool,
            simulation_id="1",
            participant_id="12",
            ability_estimator=adt.MLEstimator,
            content_balancing="WeightedPenaltyModel",
            content_balancing_args={
                "constraints": [
                    adt.Constraint(
                        "Math",
                        0.5,
                        0.2,
                        lower=0,
                        upper=1
                    ),
                    adt.Constraint(
                        "English",
                        0.5,
                        0.1,
                        lower=0,
                        upper=1
                    )
                ],
                "constraint_weight": 0.5,
                "information_weight": 0.5
            },
            debug=True
        )

        sim = adt.Simulation(adaptive_test, adt.ResultOutputFormat.CSV)
        sim.simulate()

class TestExposureControl(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)

        items = pd.DataFrame({
            "a": [1.32, 1.07, 0.84],
            "b": [-0.63, 0.18, -0.84],
            "c": [0.17, 0.10, 0.19],
            "d": [0.87, 0.93, 1],
            "id": [1, 2, 3]
        })

        self.available_items = adt.ItemPool.load_from_dataframe(items).test_items
        self.content_categories = ["Math", "English", "Math"]

        for i, _ in enumerate(self.available_items):
            self.available_items[i].additional_properties = {
                "category": [self.content_categories[i]]
            }

    def setUp(self):
        def clean_up_sim():
            path = pathlib.Path("./data/1")
            if path.exists():
                shutil.rmtree(path)
        
        self.addCleanup(clean_up_sim)
        

    def test_randomesque(self):
        item_pool = adt.ItemPool(self.available_items, 
                                 [0, 1, 0])
        

        adaptive_test = adt.TestAssembler(
            item_pool=item_pool,
            simulation_id="1",
            participant_id="12",
            ability_estimator=adt.MLEstimator,
            exposure_control="Randomesque",
            exposure_control_args={
                "n_items": 2,
                "seed": None
            },
            debug=True
        )

        sim = adt.Simulation(adaptive_test, adt.ResultOutputFormat.CSV)
        sim.simulate()


    def test_MPI_exposure_control(self):
        item_pool = adt.ItemPool(self.available_items, 
                                 [0, 1, 0])
        
        ex_args: adt.ExposureControlArgs = {
            "constraints": [
                adt.Constraint("Math", 0.5, 0.5),
                adt.Constraint("English", 0.5, 0.5)
            ],
            "participant_ids": ["1"],
            "output_format": adt.ResultOutputFormat.CSV
        }
        def run_previous_tests(sim_id: str, par_id: str):
            adaptive_test = adt.TestAssembler(
            item_pool=item_pool,
            simulation_id=sim_id,
            participant_id=par_id,
            ability_estimator=adt.MLEstimator,
            #exposure_control="MaximumPriorityIndex",
            #exposure_control_args={
            #    "n_items": 2,
            #    "seed": None
            #},
            debug=False
            )

            sim = adt.Simulation(adaptive_test, adt.ResultOutputFormat.CSV)
            sim.simulate()
            sim.save_test_results()
        run_previous_tests("1", "1")

        # acutal test
        adaptive_test = adt.TestAssembler(
            item_pool=item_pool,
            simulation_id="1",
            participant_id="2",
            ability_estimator=adt.MLEstimator,
            exposure_control="MaximumPriorityIndex",
            exposure_control_args=ex_args,
            debug=False
        )
        sim = adt.Simulation(adaptive_test, adt.ResultOutputFormat.CSV)
        sim.simulate()
        sim.save_test_results()