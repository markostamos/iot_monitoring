from __main__ import app
from utils.login_required import login_required
from flask import render_template, session


@app.route('/')
@app.route('/home')
@login_required
def index():
    user_id = session["user_id"]
    username = session["username"]
    session.clear()
    session["user_id"] = user_id
    session["username"] = username
    session["path"] = [username]
    return render_template('layout.html')
