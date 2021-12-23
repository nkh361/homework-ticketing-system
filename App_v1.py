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

def input_process(s):
    return eval(s)

app = Flask(__name__)
@app.route('/')
def start():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def post_processing():
    assignment_input = request.form['assignment']
    due_date_input = request.form['due_date']
    priority_input = request.form['priority']
    ticket = json_object(assignment_input, due_date_input, priority_input)
    ticket.send_to_json()
    return render_template('index.html', status = "Works")

@app.route('/ticket_view.html', methods=['GET'])
def read_tickets():
    with open('data.json') as datafile:
        data = datafile.read()
    return render_template('ticket_view.html', jsonfile=json.dumps(data))

def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, use_reloader = True)
main()
