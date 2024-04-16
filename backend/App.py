#!/usr/bin/env python3
from src.user import User
from src.ticket import Ticket
import mysql.connector, os, re
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from datetime import datetime

from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check
@app.route('/ping', methods=["GET"])
def ping_pong():
    return jsonify('pong!')

try:
    mysql_connector = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        database='ticketing'
    )
    print("Database connection: ", mysql_connector.is_connected())
except:
    print("MySQL connection failed.")

def validate_user(current_user: User) -> bool:
    mysql_cursor = mysql_connector.cursor()
    hash_check = current_user.hash_password()
    query = ("SELECT username FROM user WHERE username=%s AND password=%s;")
    mysql_cursor.execute(query, (current_user.username, hash_check))
    result = mysql_cursor.fetchone()
    mysql_cursor.close()
    if result is None:
        return False
    else:
        return True

def add_user(new_user: User) -> None:
    mysql_cursor = mysql_connector.cursor()
    username = new_user.username
    hashed_password = new_user.hash_password()
    user_id = new_user.user_id
    email = new_user.email
    mysql_cursor.execute(
        "INSERT INTO user (username, password, userID, email) VALUES (%s, %s, %s, %s);", (username, hashed_password, user_id, email)
    )
    mysql_connector.commit()
    mysql_cursor.close()
    print("added")

def get_user_email(username: str) -> str:
    mysql_cursor = mysql_connector.cursor()
    query = "SELECT email FROM user WHERE username='{}".format(username)
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchall()
    mysql_connector.commit()
    mysql_cursor.close()
    return result[0][2]

def get_user_id(username: str) -> None:
    mysql_cursor = mysql_connector.cursor()
    query = "SELECT user_id FROM user WHERE username='{}'".format(username)
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchall()
    mysql_connector.commit()
    mysql_cursor.close()
    return result[0][0] # result -> [('data_here',)] format. result[0][0] is data_here

def cache_info(cookie: str, data: any) -> None:
    session[cookie] = data

def date_to_int(date: str) -> int:
    year, month, day = date.split("-")
    return int(year+month+day)

def int_to_date(date: int) -> str:
    date = "{}-{}-{}".format(str(date)[:4], str(date)[4:6], str(date)[6:])
    return date

def sort_tickets(list_of_tickets: list) -> list:
    # sort the list of tickets by end time
    def sort_key(list_of_tickets: list):
        return datetime.strptime(list_of_tickets[3], '%Y-%m-%d')

    sorted_list = sorted(list_of_tickets, key=sort_key)
    last_end_time = -1
    max_weight = 0
    selected = []
    for item in sorted_list:
        """
        task = item[0]
        weight = item[1]
        start = item[2]
        end = item[3]
        status = item[4]
        """
        start = date_to_int(item[2])
        end = date_to_int(item[3])
        if start >= last_end_time:
            max_weight += item[1]
            last_end_time = end
            selected.append((item[0], item[1], int_to_date(start), int_to_date(end), item[4]))
    return selected

# test data : [('program', 9, '2023-01-12', '2023-03-04', 'in_progress'), ('sql interview prep', 10, '2023-01-12', '2023-12-10', 'open')]
# sort_tickets([('program', 9, '2023-01-12', '2023-03-04', 'in_progress'), ('sql interview prep', 10, '2023-01-12', '2023-12-10', 'open'), ('sql interview prep', 10, '2023-01-12', '2021-12-10', 'open')])

@app.route('/')
def landing() -> render_template:
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

# @app.route('/register', methods=["POST", "GET"])
# def register() -> render_template:
#     if request.method == "POST":
#         new_username = request.form['username']
#         new_password = request.form['password']
#         new_user = User(
#             username=new_username,
#             password=new_password
#         )
#         add_user(new_user)
#         cache_info("username", new_user.username)
#         cache_info("user_id", new_user.user_id)
#         return redirect(url_for('dashboard'))
#     else:
#         return render_template("register.html")
    
@app.route('/register', methods=["POST", "GET"])
def register() -> jsonify:
    if request.method == "POST":
        data = request.json
        try:
            new_username = data["username"]
            new_password = data["password"]
            new_email = data["email"]
            new_user = User(
                username=new_username,
                password=new_password,
                email=new_email
            )
            add_user(new_user)
            # print("uhh this is in post: {}".format(data))
            return jsonify({"Status": 200})

        except InterruptedError as e:
            mysql_connector.rollback()
            return jsonify({"STATUS": 200})
    
    return jsonify({"msg": "keep it get"})

@app.route("/login", methods=["POST", "GET"])
def login() -> render_template:
    if request.method == "POST":
        data = request.json
        try:
            print(data)
            current_username = data["username"]
            current_password = data["password"]
            current_email = get_user_email(current_username)
            curr_user = User(
                username=current_username,
                password=current_password,
                email = current_email
            )
            if validate_user(curr_user):
                return jsonify({"STATUS":200})
        except InterruptedError as e:
            return jsonify({e: 400})
    else:
       return jsonify({"STATUS": 400})
    

@app.route("/logout", methods=["POST", "GET"])
def logout() -> render_template:
    session.clear()
    return render_template("logout.html")

@app.route("/dashboard", methods=["POST", "GET"])
def dashboard() -> render_template:
    mysql_cursor = mysql_connector.cursor()
    if 'username' in session:
        if request.method == "POST":
            today = datetime.now()
            user_id = get_user_id(session['username'])
            new_ticket = Ticket(
                user_id=user_id,
                assignment=request.form['ticket_name'],
                created_date=today.strftime('%Y-%m-%d'),
                due_date=request.form['due_date'],
                priority=request.form['priority'],
                status=request.form['status']
            )
            mysql_cursor.execute(
                "INSERT INTO ticket (user_id, title, priority, created_at, due_date, status) VALUES (%s,%s,%s,%s,%s, %s);",
                (new_ticket.user_id, new_ticket.assignment, new_ticket.priority, new_ticket.created_date, new_ticket.due_date, new_ticket.status),
            )
            mysql_connector.commit()
            return render_template("dashboard.html", username=session['username'], status_message="Success!")
        mysql_cursor.close()
        return render_template("dashboard.html", username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route("/ticket_view", methods=["POST", "GET"])
def ticket_view() -> render_template:
    if 'username' not in session:
        return redirect(url_for('login'))
    mysql_cursor = mysql_connector.cursor()
    query = (
        "SELECT title, priority, created_at, due_date, status FROM tickets WHERE user_id='{}'".format(get_user_id(session['username']))
    )
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchall()
    if result != None:
        mysql_connector.commit()
        mysql_cursor.close()
        return render_template("ticket_view.html", results=result)
    return render_template("ticket_view.html", results=[None])

@app.route("/sorted_tickets", methods=["POST", "GET"])
def sorted_tickets():
    if 'username' not in session:
        return redirect(url_for('login'))
    mysql_cursor = mysql_connector.cursor()
    query = (
        "SELECT title, priority, created_at, due_date, status FROM tickets WHERE user_id='{}'".format(get_user_id(session['username']))
    )
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchall()
    mysql_connector.commit()
    mysql_cursor.close()
    
    sorted_results = sort_tickets(result)
    return render_template("sorted_tickets.html", results=sorted_results)
    

if __name__ == "__main__":
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, use_reloader = False)