from src.json_object import json_object
from src.database import SQL_entry
from os import path
from flask import Flask, request, render_template, jsonify
import json

app = Flask(__name__)

@app.route("/")
def root_page():
    return render_template('index.html')

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

    return "Entered Successfully!"

@app.route('/all.html', methods = ['GET'])
def show_data():
    # create entry with existing sql
    SQL_stuff = SQL_entry()
    SQL_stuff.create_entry()
    query = SQL_stuff.read_entry()
    return jsonify(query)

"""
TODO and notes:
    finished makin this work, just need to make it look nice. and not like a json file :D
    need to make a ticket sorting thing (like dropdown menu)
    need to make a ticket search thing
"""

def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, use_reloader = False)

main()
