from src.user import User
from src.ticket import Ticket
import mysql.connector, os, datetime
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

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
    query = ("SELECT username FROM users WHERE username=%s AND password=%s;")
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
    mysql_cursor.execute(
        "INSERT INTO users (username, password, user_id) VALUES (%s, %s, %s);", (username, hashed_password, user_id)
    )
    mysql_connector.commit()
    mysql_cursor.close()
    print("added")

def get_user_id(username: str) -> None:
    mysql_cursor = mysql_connector.cursor()
    query = "SELECT user_id FROM users WHERE username='{}'".format(username)
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchall()
    mysql_connector.commit()
    mysql_cursor.close()
    return result[0][0] # result -> [('data_here',)] format. result[0][0] is data_here

def cache_info(cookie: str, data: any) -> None:
    session[cookie] = data

def sort_tickets(list_of_tickets: list) -> list:
    # TODO
    list_of_tickets.sort(key=lambda x: int(x[2].strftime('%Y%m%d')))
    max_weight, current_end = 0, 0
    sorted_tickets = []
    for ticket in list_of_tickets:
        # SELECT title, priority, created_at, due_date, status FROM tickets WHERE user_id=
        if ticket[2] >= current_end:
            current_end = ticket[3]
            max_weight += ticket[1]
        print(max_weight)

# test data : [('program', 9, '2023-01-12', '2023-03-04', 'in_progress'), ('sql interview prep', 10, '2023-01-12', '2023-12-10', 'open')]
# sort_tickets([('program', 9, '2023-01-12', '2023-03-04', 'in_progress'), ('sql interview prep', 10, '2023-01-12', '2023-12-10', 'open')])

@app.route('/')
def landing() -> render_template:
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=["POST", "GET"])
def register() -> render_template:
    if request.method == "POST":
        new_username = request.form['username']
        new_password = request.form['password']
        new_user = User(
            username=new_username,
            password=new_password
        )
        add_user(new_user)
        cache_info("username", new_user.username)
        cache_info("user_id", new_user.user_id)
        return redirect(url_for('dashboard'))
    else:
        return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login() -> render_template:
    if request.method == "POST":
        current_username = request.form['username']
        current_password = request.form['password']
        if validate_user(User(username=current_username, password=current_password)):
            cache_info("username", current_username)
            return redirect(url_for('dashboard'))
        else:
            error = "invalid username or password"
            return render_template("login.html", error=error)
    return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout() -> render_template:
    session.clear()
    return render_template("logout.html")

@app.route("/dashboard", methods=["POST", "GET"])
def dashboard() -> render_template:
    mysql_cursor = mysql_connector.cursor()
    if 'username' in session:
        if request.method == "POST":
            today = datetime.datetime.now()
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
                "INSERT INTO tickets (user_id, title, priority, created_at, due_date, status) VALUES (%s,%s,%s,%s,%s, %s);",
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
    mysql_connector.commit()
    mysql_cursor.close()
    # print("RESULT: ", result)
    return render_template("ticket_view.html", results=result)

# @app.route("/sorted_tickets", methods=["POST", "GET"])
# def sorted_tickets():
#     return

def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, use_reloader = True)
main()
