from src.json_object import json_object
from os import path
from flask import Flask, request, render_template, jsonify, redirect, url_for, g, abort
import json, sqlite3, os, datetime
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
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

@app.route("/")
def root_page():
    return render_template('login.html')

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
