import sqlite3, json, datetime, os
import pandas as pd
from os import path

sql_file = 'assignments.db'

def create_entry_sql():
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
    df_assignments = pd.json_normalize(data, record_path=['assignments'])
    # sql stuff starts here
    conn = sqlite3.connect(sql_file)
    df_assignments.to_sql('assignments', conn, if_exists='replace')

def display_all_assignments():
    conn = sqlite3.connect(sql_file)
    cur = conn.cursor()
    sql_statement = "SELECT * FROM assignments"
    query = cur.execute(sql_statement)
    return query.fetchall()
