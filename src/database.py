import sqlite3, json, os
from os import path

sql_file = 'assignments.db'

class SQL_entry():
    def __init__(self):
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        df_assignments = pd.json_normalize(data, record_path = ['assignments'])
        ## To be continued
