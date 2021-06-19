import sqlite3, json, os
import pandas as pd
from datetime import date
from os import path

# create json object

class json_object:
    def __init__(self, assignment, due_date, priority):
        self.assignment = input("Enter an assignment name: ")
        self.due_date = input("Enter the assignment due date: ")
        self.priority = input("Enter the assignment priority: ")

    def show_object(self):
        return self.assignment, self.due_date, self.priority
    
    def send_to_json(self):
        data = {}
        data['assignments'] = []
        if path.exists('data.json') == False:
            with open('data.json', 'w') as outfile:
                ID = self.gen_ID()
                data['assignments'].append({
                    'ID': ID + 1,
                    'Assignment': self.assignment,
                    'Due Date': self.due_date,
                    'Priority': self.priority
                    })
                outfile.seek(0) # reset the file pointer to index 0
                json.dump(data, outfile)
            print("success!")
        else:
            pass
        
    def gen_ID(self):
        return 0

def main():
    j_object = json_object("homework", "3-1-2", 1)
    # a = j_object.show_object()
    # print(a)
    j_object.send_to_json()

main()

