import sqlite3, json, database, os
import pandas as pd
from flask import Flask, request
from datetime import date
from os import path

"""
Shit notes:
    SQL and Queries work
    SQL table 'assignments' work
"""

def create_entry_json():
    # temp prototyping to make sure creating entries works
    class_title = input("Enter a class: ")
    assignment = input("Enter assignment name: ")
    difficulty = input("Enter difficulty on scale 1-10: ")
    status = input("Enter assignment status: ")
    time_completion = input("Enter time required to complete: ")
    entry_date = str(date.today())
    data = {}
    data['assignments'] = [] 
    if path.exists('data.json') == False:
        with open('data.json', 'w') as outfile: 
            ID = gen_ID()
            data['assignments'].append({
                'ID': ID + 1,
                'creation date': entry_date,
                'class': class_title,
                'assignment': assignment,
                'difficulty': difficulty,
                'status': status,
                'time to complete': time_completion
                })
            json.dump(data, outfile)
        print("success!")
    else:
        with open('data.json', 'r+') as outfile:
            ID = gen_ID()
            json_dict = json.load(outfile) # turns json object to python dictionary
            json_dict['assignments'].append({
                'ID': ID + 1,
                'creation date': entry_date,
                'class': class_title,
                'assignment': assignment,
                'difficulty': difficulty,
                'status': status,
                'time to complete': time_completion
                })
            outfile.seek(0) # reset the file pointer to position 0
            json.dump(json_dict, outfile, indent=4)
        print("success")
    return class_title, assignment, difficulty, status, time_completion, entry_date

def gen_ID():
    file_size = os.path.getsize('data.json')
    if file_size <= 2:
        ID = 0
    else:
        f = open('data.json')
        json_file = json.load(f)
        for element in json_file['assignments']:
            ID = element['ID']        
    return ID


# class_name, assignment, diffic, stat, time_compl, entry_ = create_entry_json()
# print(class_name, assignment, diffic, stat, time_compl, entry_)
# flatten the json data
create_entry_json()
with open('data.json', 'r') as f:
    data = json.loads(f.read())

df_nested_json = pd.json_normalize(data, record_path=['assignments'])
print(df_nested_json)
