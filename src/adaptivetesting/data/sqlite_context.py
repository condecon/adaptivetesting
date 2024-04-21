from typing import List
from ..models.test_result import TestResult
from ..services.test_results_interface import ITestResults
import sqlite3


class SQLiteContext(ITestResults):
    """Implements ITestResults interface for
    saving test results to SQLITE."""

    def __init__(self, simulation_id: str, participant_id: int):
        super().__init__(simulation_id, participant_id)

    def save(self, test_results: List[TestResult]) -> None:
        """Saves test results to SQLITE file
        :param test_results: test results from adaptive test"""

        try:
            con = sqlite3.connect(self.filename)
        except sqlite3.OperationalError:
            con = sqlite3.connect(f"../{self.filename}")

        cur: sqlite3.Cursor = con.cursor()
        # create table
        self._create_table(cur)
        # insert test results into table
        for result in test_results:
            sql_query = f"""
            INSERT INTO p_{self.participant_id}
            VALUES ("{result.test_id}", 
            {result.ability_estimation}, 
            {result.standard_error},
            {result.showed_item}, 
            {result.response}, 
            {result.true_ability_level})"""
            cur.execute(sql_query)
        # commit changes
        con.commit()
        # close connection
        con.close()

    def load(self) -> List[TestResult]:
        """Loads test results from SQLITE file"""
        raise NotImplementedError("This  function is not implemented.")

    def _create_table(self, cur: sqlite3.Cursor) -> None:
        """Creates test results table"""
        sql_query = f"""CREATE TABLE IF NOT EXISTS p_{self.participant_id} (
            test_id,
            ability_estimation,
            standard_error,
            showed_item,
            response,
            true_ability_level
            )"""
        cur.execute(sql_query)
