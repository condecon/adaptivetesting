from typing import List
from ..models.__test_result import TestResult
from ..services.__test_results_interface import ITestResults
import sqlite3


class SQLiteContext(ITestResults):
    def __init__(self, simulation_id: str, participant_id: int):
        """Implementation of the ITestResults interface for
        saving test results to a SQLITE database.
        The resulting sqlite file <simulation_id>.db
        will be of the SQLITE3 format.

        Args:
            simulation_id (str): db filename

            participant_id (int): participant id and table name
        """
        super().__init__(simulation_id, participant_id)

    def save(self, test_results: List[TestResult]) -> None:
        """Saves a list of test results to the database
        in the table <participant_id>.

        Args:
            test_results (List[TestResult]): list of test results
        """
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
            VALUES ("{result.test_id}", {result.ability_estimation}, {result.standard_error},
            {result.showed_item}, {result.response}, {result.true_ability_level})"""
            cur.execute(sql_query)
        # commit changes
        con.commit()
        # close connection
        con.close()

    def load(self) -> List[TestResult]:
        """Loads results from the database.
        The implementation of this method is required
        by the interface. However, is does not have
        any implemented functionality and will throw an error.

        Returns: List[TestResult]
        """
        raise NotImplementedError("This  function is not implemented.")

    def _create_table(self, cur: sqlite3.Cursor) -> None:
        """Creates a table in the database with the
        name <participant_id> if it does not exist.

        Args:
            cur (sqlite3.Cursor): database cursor
        """
        sql_query = f"""CREATE TABLE IF NOT EXISTS p_{self.participant_id} (
            test_id,
            ability_estimation,
            standard_error,
            showed_item,
            response,
            true_ability_level
            )"""
        cur.execute(sql_query)
