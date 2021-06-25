import sqlite3, json, os
from os import path
import pandas as pd

sql_file = 'assignments.db'

class SQL_entry():
    def create_entry(self):
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        df_assignments = pd.json_normalize(data, record_path = ['assignments'])
        conn = sqlite3.connect(sql_file)
        df_assignments.to_sql('assignments', conn, if_exists = 'replace')

    def read_entry(self):
        conn = sqlite3.connect(sql_file)
        cur = conn.cursor()
        sql_statement = 'SELECT * FROM assignments'
        query = cur.execute(sql_statement)
        return query.fetchall()

   
    def update_entry(self, ID):
        conn = sqlite3.connect(sql_file)
        cur = conn.cursor()
        # sql_statement = "SELECT * FROM assignments WHERE ID={}".format(ID)
        # query = cur.execute(sql_statement)
        update = input("What would you like to update: 1 - assignment 2 - due date 3 - priority: ")
        if update == "1":
            assignment_updated_entry = input("Enter updated assignment: ")
            sql_assignment_updated = 'UPDATE assignments SET assignment = "{}" WHERE ID = {}'.format(assignment_updated_entry, str(ID))
            query = cur.execute(sql_assignment_updated)
            conn.commit()
        if update == "2":
            due_date_updated_entry = input("Enter updated due date: ")
            sql_due_date_update = 'UPDATE assignments SET "Due Date" = "{}" WHERE ID = {}'.format(due_date_updated_entry, str(ID))
            query = cur.execute(sql_due_date_update)
            conn.commit()
        if update == "3":
            priority_updated_entry = input("Entere updated priority: ")
            sql_priority_updated = 'UPDATE assignments SET priority = "{}" WHERE ID = {}'.format(priority_updated_entry, str(ID))
            query = cur.execute(sql_priority_updated)
            conn.commit()
        print(self.read_entry())
    
    def delete_entry(self, ID):
        """
        conn = sqlite3.connect(sql_file)
        cur = conn.cursor()
        delete = input("What would you like to delete")
        """
        pass


def main():
    a = SQL_entry()
    a.update_entry(2)

main()
