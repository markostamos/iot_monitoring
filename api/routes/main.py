from __main__ import app
from utils.login_required import login_required
from flask import render_template
@app.route('/')
@app.route('/home')
@login_required
def index():
    return render_template('layout.html')


