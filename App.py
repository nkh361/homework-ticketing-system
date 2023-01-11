from src.user import User
from src.ticket import Ticket
import mysql.connector, os, datetime
from flask import Flask, request, render_template, jsonify, redirect, url_for, g, abort, session

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

mysql_cursor = mysql_connector.cursor()

def validate_user(current_user: User):
    hash_check = current_user.hash_password()
    query = ("SELECT username FROM users WHERE username=%s AND password=%s;")
    mysql_cursor.execute(query, (current_user.username, hash_check))
    mysql_cursor.commit()
    result = mysql_cursor.fetchone()
    if result is None:
        return False
    else:
        return True

def add_user(new_user: User):
    username = new_user.username
    hashed_password = new_user.hash_password()
    user_id = new_user.user_id
    mysql_cursor.execute(
        "INSERT INTO users (username, password, user_id) VALUES (%s, %s, %s);", (username, hashed_password, user_id)
    )
    mysql_connector.commit()
    print("added")

def get_user_id(username):
    query = "SELECT user_id FROM users WHERE username='%s'"
    mysql_cursor.execute(query, username)
    result = mysql_cursor.fetchall()
    return result # TODO: not returning any results

def cache_info(cookie: str, data: any) -> None:
    session[cookie] = data

@app.route('/')
def landing():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=["POST", "GET"])
def register():
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
def login():
    if request.method == "POST":
        current_username = request.form['username']
        current_password = request.form['password']
        if validate_user(User(username=current_username, password=current_password)):
            # session['username'] = current_username
            cache_info("username", current_username)
            return redirect(url_for('dashboard'))
        else:
            error = "invalid username or password"
            return render_template("login.html", error=error)
    return render_template("login.html")

@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    if 'username' in session:
        if request.method == "POST":
            today = datetime.datetime.today()
            new_ticket = Ticket(
                user_id="1673304387-554",
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
        return render_template("dashboard.html", username=session['username'])
    else:
        return redirect(url_for('login'))

# @app.route("/ticket_view", methods=["POST", "GET"])
# def ticket_view():
#     # REMINDER: set post method in ticket_view.html
#     return render_template('ticket_view.html')
#     # <p><input type=text name=ticket_name placeholder="Title"></p>

def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, use_reloader = True)
main()
