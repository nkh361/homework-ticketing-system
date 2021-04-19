import datetime, sqlite3, json, database 
from flask import Flask, request
from os import path

def create_DB():
  if database.checkforDB() is False:
    database.createRDB()
  else:
    pass

def create_entry():
  # temp prototyping to make sure creating entries works
  class_title = input("Enter a class: ")
  assignment = input("Enter assignment name: ")
  difficulty = input("Enter difficulty on scale 1-10: ")
  status = input("Enter assignment status: ")
  data = {}
  data['assignments'] = []
  ID = gen_ID()
  data['assignments'].append({
      'ID': ID + 1,
      'class': class_title,
      'assignment': assignment,
      'difficulty': difficulty,
      'status': status
      })
  print("success!")
  if path.exists('data.json') == False:
    with open('data.json', 'w') as outfile:
      json.dump(data, outfile)
  else:
    with open('data.json', 'a') as outfile:
      json.dump(data, outfile)
  return outfile



def gen_ID():
  f = open('data.json')
  json_file = json.load(f)
  if json_file 
  ID = len(json_file['assignments'])
  return ID

