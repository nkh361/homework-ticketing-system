import sqlite3, json, os
import pandas as pd
from datetime import date
from os import path
from dataclasses import dataclass

@dataclass
class json_object:
    username: str
    assignment: str
    start_date: str
    due_date: str
    priority: str
    
    def send_to_json(self):
        weights = {"low": 1, "mid": 3, "high": 5, "Not assigned": 0}
        data = {}
        data['assignments'] = []

        def get_weight():
            return weights[self.priority]

        try:
            if path.exists('data.json') == False:
                with open('data.json', 'w') as outfile:
                    ID = self.gen_ID()
                    # possibly use uuid, just send to file and check if its in
                    data['assignments'].append({
                        'Username': self.username,
                        'ID': ID + 1,
                        'Assignment': self.assignment,
                        'Start Date': self.start_date,
                        'Due Date': self.due_date,
                        'Priority': get_weight()
                        })
                    outfile.seek(0) # reset the file pointer to index 0
                    json.dump(data, outfile, indent=4)

            else:
                with open('data.json', 'r+') as outfile:
                    ID = self.gen_ID()
                    json_dict = json.load(outfile)
                    json_dict['assignments'].append({
                        'Username': self.username,
                        'ID': ID + 1,
                        'Assignment': self.assignment,
                        'Start Date': self.start_date,
                        'Due Date': self.due_date,
                        'Priority': get_weight()
                    })
                    outfile.seek(0)
                    json.dump(json_dict, outfile, indent=4)
                    print("success!")
        except:
            print("json push error")

        
    def gen_ID(self):
        if (path.exists('data.json') == False) or (os.path.getsize('data.json')<=2):
            return 0 # json file DNE or empty json file
        else:
            f = open('data.json')
            json_file = json.load(f)
            for element in json_file['assignments']:
                ID = element['ID']
            return ID

