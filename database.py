import sqlite3, json, datetime 
from os import path

def createRDB():
 con = sqlite3.connect('assignments.db')
 cur = con.cursor()
 table_create = 'CREATE TABLE assigments (ID int, CLASS_TITLE text, ASSIGNMENT text, DIFFICULTY i    nt, STATUS text)'
 con.commit()
 con.close()

def checkforDB():
  if path.exists('assignments.db') == False:
    createRDB()
    return False
  else:
    return True

def create_entry_RDB():
  json_file = open('data.json')
  data = json.load(json_file)
  for entry in data['class']:
    print(entry)
  json_file.close()

create_entry_RDB()
