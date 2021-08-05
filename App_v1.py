from flask import Flask, render_template, request, session, redirect, url_for, g, abort

app = Flask(__name__)
app.secret_key = 'secret'

class User:
    def __init__(self, ID, username, password):
        self.id = ID
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

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
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, use_reloader = False)
main()

