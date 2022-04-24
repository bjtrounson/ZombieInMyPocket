import os
import unittest

from sql_manager.sql_manager import SQLManager
from sqlite3 import Connection


class SQLManagerTestCases(unittest.TestCase):
    def setUp(self) -> None:
        self.current_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.conn = SQLManager.create_connection(f"{self.current_dir}/game_data.db")
        self.sql_manager = SQLManager()

    def test_when_sql_manager_creates_connection_expect_connection(self):
        conn = SQLManager.create_connection(f"{self.current_dir}/game_data.db")
        self.assertTrue(isinstance(conn, Connection))  # add assertion here

    def test_when_sql_manager_creates_tables_expect_tables_in_db(self):
        self.sql_manager.create_tables(self.conn)
        query = """SELECT * FROM item"""
        cur = self.conn.cursor()
        cur.execute(query)
        print(cur.fetchall())


if __name__ == '__main__':
    unittest.main()
