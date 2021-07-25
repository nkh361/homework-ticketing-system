from src.json_object import json_object
from src.database import SQL_entry
from os import path
from flask import Flask, request, render_template

"""
tasks: 
    fix calls to json_object.py
    fix calls to database.py
        - to text input from flask
"""

json_data = "src/data.json"

class Server:
    def __init__(self):
        self.test_ = "Hello, world!"

app = Flask(__name__)

@app.route("/")
def root_page():
    return render_template('index.html')


# send text field data to json_object.py


@app.route('/', methods = ['POST'])
def test_json():
    """
    HTML input name will be 'assignment', 'due_date', and 'priority'
    """
    assignment = request.form['assignment']
    due_date = request.form['due_date']
    priority = request.form['priority']
    
    json = json_object(assignment, due_date, priority)
    json.send_to_json()

    print("win!")
    return json.show_object()

def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, use_reloader = False)

main()
