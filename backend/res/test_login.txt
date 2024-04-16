# create a flask app

import flask

app = flask.Flask(__name__)
app.secret_key = 'password'

# login manager

import flask_login

login_manager = flask_login.LoginManager()
login_manager.init_app(app) # tells the login manager about the existing flask app

# mock database

users = {'foo@bar.tld': {'password': 'secret'}} # flask-login doesnt care how its stored, only
                                                # whats retrieved

# how to load a user

class User(flask_login.UserMixin):
    """
    define the user object
    """
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

# define the view

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method = 'GET':
        return '''
                <form action = 'login' methods = 'POST'>
                <input type = 'text' name = 'email' id = 'email' placeholder = 'email'/>
                <input type = 'password' name = 'password' id = 'password' placeholder = 'password'/>
                <input type = 'submit' name = 'submit'/>
                </form>
                ''' # would replace with a template

    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protexted'))

    return 'Bad Login'

@app.route('/protected')
@flask_login.login_required
def protexted():
    return 'Logged in as: ' + flask_login.current_user.id

# clear the session and log user out

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

# login failure
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'















