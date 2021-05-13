import sqlite3, json, datetime, os
import pandas as pd
from os import path

sql_file = 'assignments.db'

def create_entry_sql():
    """
    convert JSON data to pandas dataframe, then use to_sql for sql conversion
    """
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
    df_assignments = pd.json_normalize(data, record_path=['assignments'])
    # sql stuff starts here
    conn = sqlite3.connect(sql_file)
    df_assignments.to_sql('assignments', conn, if_exists='replace')

def display_all_assignments():
    """
    Select all query
    """
    conn = sqlite3.connect(sql_file)
    cur = conn.cursor()
    sql_statement = "SELECT * FROM assignments"
    query = cur.execute(sql_statement)
    return query.fetchall()

def show_assignments():
    """
    Select all assignments query
    """
    conn = sqlite3.connect(sql_file)
    cur = conn.cursor()
    sql_statement = "SELECT assignment FROM assignments"
    query = cur.execute(sql_statement)
    return query.fetchall()

