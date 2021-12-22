import sqlite3, json, os
import pandas as pd
from datetime import date
from os import path
from dataclasses import dataclass

@dataclass
class json_object:
    assignment: str
    due_date: str
    priority: str

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
                json.dump(data, outfile, indent=4)

        else:
            with open('data.json', 'r+') as outfile:
                ID = self.gen_ID()
                json_dict = json.load(outfile)
                json_dict['assignments'].append({
                    'ID': ID + 1,
                    'Assignment': self.assignment,
                    'Due Date': self.due_date,
                    'Priority': self.priority
                })
                outfile.seek(0)
                json.dump(json_dict, outfile, indent=4)
                print("success!")

        
    def gen_ID(self):
        if (path.exists('data.json') == False) or (os.path.getsize('data.json')<=2):
            return 0 # json file DNE or empty json file
        else:
            f = open('data.json')
            json_file = json.load(f)
            for element in json_file['assignments']:
                ID = element['ID']
            return ID

# def main():
#     A = json_object("test123", "12-12-12", "top")
#     A.send_to_json()
# main()

