import json_file, database, os
from os import path
from flask import Flask, request, render_template

def check_for_db():
    if os.path.exists('assignments.db') == False:
        print("hazzah!")
    else:
        print("poo")

def create_entry():
    """
    creates entries for both JSON and SQL table 'assignments'
    """
    json_file.create_entry_json()
    database.create_entry_sql()

app = Flask(__name__)
@app.route('/')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def display():
    """
    returns SQL query to client
    """
    data_db = database.display_all_assignments()
    # data_str = str()
    """
    for i in range(len(data_db)):
        for entry in data_db:
            data_str += str(entry[i]) + ' , '
        if i == 7:
            data_str += '\n'
            i = 0
    """
    return render_template('index.html', data = data_db)

def main():
    # create_entry()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, use_reloader = True)

main()


