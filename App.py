from src.json_object import json_object
from src.database import SQL_entry
from os import path
from flask import Flask, request, render_template
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

"""
TODO:
    create SQL entry for assignments
    fix show_data()
        not showing json stuff
    or
        can query from database and display data from there
"""

@app.route('/all.html', methods = ['GET'])
def show_data():
    json_file = 'data.json'
    return render_template('all.html', title="tickets", jsonfile=json.dumps(json_file))

def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, use_reloader = False)

main()
