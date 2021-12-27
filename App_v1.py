from flask import Flask, render_template, request, session, redirect, url_for, g, abort
import sqlite3, json, os
from os import path
from dataclasses import dataclass
from src.json_object import json_object
import pandas as pd
@dataclass
class User:
    username: str
    password: str
    # str path to usr_data.json
    # tickets: str

def input_process(s):
    return eval(s)

app = Flask(__name__)
@app.route('/')
def start():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def post_processing():
    # testing username
    username_input = "nathan"
    assignment_input = request.form['assignment']
    start_input = request.form['start_date']
    due_date_input = request.form['due_date']
    priority_input = str(request.form.get('priority'))
    ticket = json_object(username_input, assignment_input, start_input, due_date_input, priority_input)
    ticket.send_to_json()
    return render_template('index.html', status = "Works")

@app.route('/ticket_view.html', methods=['GET'])
# weighted interval scheduling
def read_tickets():
    file = open('data.json')
    data = json.load(file)
    file.close()
    columns = ["Username", "ID", "Assignment", "Start Date", "Due Date", "Priority"]
    df = pd.DataFrame(data["assignments"], columns=columns)
    table = df.to_html(index=False)
    return render_template('ticket_view.html', table=table)

def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, use_reloader = True)
main()
