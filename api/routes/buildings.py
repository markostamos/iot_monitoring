from __main__ import app,mongo
from utils.login_required import login_required
from flask import render_template,session

@app.route('/buildings')
@login_required
def buildings():
    buildings = list(mongo.db.buildings.find(
        {'user_id':session['user_id']}))
    return render_template('buildings.html', buildings=buildings)


@app.route('/buildings/<id>/<name>/<user_id>')
@login_required
def building(id,name,user_id):
    
    if user_id != session["user_id"]:
        return "BADDDDD"

    session["building_id"] = id
    session["building_name"] = name
    
    devices = list(mongo.db.devices.find(
        {'building_id': session['building_id']}))

    return render_template('devices.html',devices=devices)
    