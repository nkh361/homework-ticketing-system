import sqlite3, json, datetime 
import os
from os import path

def createRDB():
    con = sqlite3.connect('assignments.db')
    cur = con.cursor()
    table_create = 'CREATE TABLE assigments (ID int, CLASS_TITLE text, ASSIGNMENT text, DIFFICULTY int, STATUS text)'
    con.commit()
    con.close()

def checkforDB():
    if path.exists('assignments.db') == False:
        createRDB()
        return False
    else:
        return True

def create_entry_sql():
    f = open('data.json')
    json_file = json.load(f)
    print(json_file['assignments'])

create_entry_sql()
