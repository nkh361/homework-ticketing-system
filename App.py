import datetime, sqlite3, json
from os import path
from flask import Flask, request

"""
 things i need:
 - sql RDB
 - flask
 
 sql fields:
 - ID
 - class title
 - assignment name
 - difficulty
 - status

 schedule jobs by diffuclty
"""

def createRDB():
 con = sqlite3.connect('assignments.db')
 cur = con.cursor()
 table_create = 'CREATE TABLE assigments (ID int, CLASS_TITLE text, ASSIGNMENT text, DIFFICULTY int, STATUS text)'
 con.commit()
 con.close()

def checkforDB():
  if path.exists('assignments.db') == False:
    createRDB()
  else:
    create_entry()

def create_entry():
  # temp prototyping to make sure creating entries works
  class_title = input("Enter a class: ")
  assignment = input("Enter assignment name: ")
  difficulty = input("Enter difficulty on scale 1-10: ")
  status = input("Enter assignment status: ")
  data = {}
  data['assignments'] = []
  data['assignments'].append({
      'class': class_title,
      'assignment': assignment,
      'difficulty': difficulty,
      'status': status
      })
  print("success!")
  with open('data.txt', 'a') as outfile:
    json.dump(data, outfile)

create_entry()
