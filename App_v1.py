from flask import Flask, render_template, request, session, redirect, url_for, g, abort
import sqlite3, json, os, datetime
from os import path
from src.json_object import json_object
import pandas as pd
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'test'
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
# reload the user object from the user ID stored in the session
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    # ticket_data = db.Column(JSON, nullable=True)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("The username is taken.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

def input_process(s):
    return eval(s)

@app.route('/ticket-dash')
def start():
    return render_template('index.html')

def weighted_scheduling():
    # 7th lecture
    """
    Optimal: schedule where jobs are ordered according to non-decreasing processing times

    Analyzing cost difference: the cost goes down if this difference is greater than 0
            - if processing time of job i > processing time of job j
            - schedule where jobs are ordered according to non-decreasing ratio p_i / w_i is
              optimal
    """
    file = open('data.json')
    data = json.load(file)
    file.close()
    columns = ["Username", "ID", "Assignment", "Start Date", "Due Date", "Priority"]
    # df = pd.DataFrame(data["assignments"], columns=columns)
    # table = df.to_html(index=False)
    polished_data = dict()
    for i in data["assignments"]:
        # print(i["Priority"])
        polished_data.update({i["Assignment"]: i["Priority"]})
    print(polished_data)
    # TODO: make integer value of processing time, sort the dictionary by p_i / w_i
weighted_scheduling()


# TODO: FIX THIS
@app.route('/ticket-dash', methods=['POST'])
@login_required
def post_processing():
    json_query = {
            "assignments": [
                {
                    "Ticket ID": gen_ID(),
                    "Assignment": form.assignment,
                    "Start Date": form.start_date,
                    "End Date": form.end_date,
                    "Priority": form.priority,
                }
            ]
    }
    user = current_user.name
    a = db.session.query(current_user)
    a = a.filter(current_user.name == current_user.name)
    record = a.one()
    record.ticket_data = json_query
    db.session.commit()
    # TODO: finish this function garbage, restart database table to allow json column
    # IDEA: utilize a form for each input, but if input is blank then default NULL
    # use request.form.to_dict(flat = False) to get a dictionary with lists of values
    # TODO: set weights to start date - end date * priority score
    return json_query

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # check if the user is in the database or not, if they are
        # then check their password hash
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    print("Current: ", current_user)
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')
    # TODO: redirect yarn server, yarn server pull JSON from flask

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/ticket_view.html', methods=['GET'])
# weighted interval scheduling
def read_tickets():
    file = open('data.json')
    data = json.load(file)
    file.close()
    columns = ["Username", "ID", "Assignment", "Start Date", "Due Date", "Priority"]
    df = pd.DataFrame(data["assignments"], columns=columns)
    table = df.to_html(index=False)
    return render_template('ticket_view.html', table=table)

def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, use_reloader = True)
main()
