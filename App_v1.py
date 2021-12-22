from flask import Flask, render_template, request, session, redirect, url_for, g, abort
import sqlite3, json, os
from os import path
from dataclasses import dataclass
from src.json_object import json_object

@dataclass
class User:
    username: str
    password: str
    # str path to usr_data.json
    # tickets: str

@dataclass
class User_Actions(User):
    def create_ticket(ff_assignment, ff_due_date, ff_priority):
        return json_object(ff_assignment, ff_due_date, ff_priority)

def input_process(s):
    return eval(s)

app = Flask(__name__)
@app.route('/')
def start():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def post_processing():
    assignment_input = input_process(request.form['assignment'])
    due_date_input = input_process(request.form['due_date'])
    priority_input = input_process(request.form['priority'])
    Sample_user = User_Actions(username='nate', password='test')
    Sample_ticket = Sample_user.create_ticket(assignment_input, due_date_input, priority_input)
    Sample_ticket.send_to_json()
    return render_template('index.html', status = "Works")

def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, use_reloader = True)
main()
