from flask import Flask, render_template, request, session, redirect, url_for, g, abort
import sqlite3, json, os
from os import path

app = Flask(__name__)
app.secret_key = 'secret'

relational_database = 'tickets.db'

class User:
    def __init__(self, ID, username, password):
        self.ID = ID
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

    def user_table_genisis(self):
        conn = sqlite3.connect(relational_database)
        cur = conn.cursor()
        query = cur.execute('CREATE TABLE Users (ID int, username text, password text)')
        conn.commit()

    def user_table_count(self):
        conn = sqlite3.connect(relational_database)
        cur = conn.cursor()
        query = cur.execute('SELECT COUNT(*) FROM Users')
        count = query.fetchone()[0]
        return count
    
    def create_table_for_users(self):
        conn = sqlite3.connect(relational_database)
        cur = conn.cursor()

        if self.user_table_count() == 0 or '0':
            sql_statement = 'CREATE TABLE Users (ID int, username text, password text)'
            query = cur.execute(sql_statement)
            
        conn.commit()

    def create_user_entry(self):
        conn = sqlite3.connect(relational_database)
        cur = conn.cursor()
        sql = 'INSERT INTO Users (ID, username, password) VALUES (%d, %s, %s)'
        val = (self.ID, self.username, self.password)
        cur.execute(sql, val)
        conn.commit()

    def get_all_users(self):
        conn = sqlite3.connect(relational_database)
        cur = conn.cursor()
        query = cur.execute('SELECT * FROM Users')
        for x in query.fetchall():
            print(x)

# list of users

users = []
users.append(User(ID = 1, username = 'nathan', password = 'test'))
users.append(User(ID = 2, username = 'nkh', password = 'nkh'))

@app.before_request
def before_request():
    if 'user_id' in session:
        user = [x for x in users if x.ID == session['user_id']][0]
        g.user = user
    else:
        g.user = None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.ID
            return redirect(url_for('profile'))
        
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/test', methods=['POST'])
def test():
    # left off here
    tmp = User()
    # tmp.

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

def main():
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.run(debug = True, use_reloader = False)
    user = User(ID = 3, username = 'test', password = 'test')
    user.user_table_genisis()
    user.create_table_for_users()

main()

