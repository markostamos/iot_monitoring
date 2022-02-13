
from __main__ import app, mongo
from flask import session, url_for, redirect, render_template, request
import bcrypt


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        existing_user = mongo.db.users.find_one(
            {'email': request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())

            mongo.db.users.insert_one({
                'username': request.form['username'],
                'email': request.form['email'],
                'password': hashpass
            })

            return redirect(url_for('login'))

        return 'That email already exists!'
    else:
        if session.get("username"):
            return redirect(url_for('index'))
        else:
            return render_template('register.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})
        if login_user:

            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['username'] = login_user['username']
                session['user_id'] = str(login_user.get('_id'))
                return redirect(url_for('index'))
            else:
                return 'Invalid username/password combination'
    else:
        if session.get("username"):
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
