import unittest
import sys
import mysql.connector

sys.path.append('..')
from App import app

class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.connector = mysql.connector.connect(
            host = '127.0.0.1',
            user = 'root',
            database = 'ticketing'
        )
        self.cursor = self.connector.cursor()
    
    def test_tables(self):
        self.cursor.execute("show tables;")
        result = self.cursor.fetchall()
        self.assertEqual(result, [('tickets',), ('users',)])

if __name__ == "__main__":
    unittest.main()