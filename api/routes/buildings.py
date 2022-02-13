from __main__ import app, mongo
from utils.login_required import login_required
from flask import render_template, session, url_for, request, redirect


@app.route('/buildings/new_building', methods=["POST"])
@login_required
def new_building():

    mongo.db.buildings.insert_one({
        'name': request.form['name'],
        'location': request.form['location'],
        'user_id': session['user_id']
    })

    return redirect(url_for('dashboard', chosen_building=request.form["name"]))


@app.route('/delete_building', methods=["POST"])
@login_required
def delete_building():
    building_name = request.form["building_name"]
    print(building_name)
    mongo.db.buildings.delete_one({
        'name': building_name,
        'user_id': session["user_id"]
    })

    mongo.db.devices.delete_many({
        'building_name': building_name,
        'user_id': session["user_id"]
    })
    mongo.db.notifications.delete_many({
        'building': building_name,
        'user_id': session["user_id"]
    })

    return "Success"
