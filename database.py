import sqlite3, json, datetime

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
  
