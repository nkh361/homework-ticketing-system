from src.json_object import json_object
from src.database import SQL_entry
from os import path
from flask import Flask, request, render_template

json_data = "src/data.json"

class Server:
    def __init__(self):
        self.test_ = "Hello, world!"

app = Flask(__name__)

@app.route("/")
def root_page():
    return render_template('index.html')

def main():
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.run(debug = True, use_reloader = False)

main()
