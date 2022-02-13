
from __main__ import app, mongo
from flask import session, render_template, request, redirect, url_for
from utils.login_required import login_required


@app.route('/new_device', methods=["POST"])
@login_required
def new_device():
    mongo.db.devices.insert_one({
        'name': request.form['name'],
        'type': request.form['type'],
        'building_name': request.form["building_name"],
        'user_id': session['user_id']
    })

    return redirect(url_for("dashboard", chosen_building=request.form["building_name"], chosen_device=request.form["name"]))


@app.route('/delete_device', methods=["POST"])
@login_required
def delete_device():

    mongo.db.devices.delete_one({
        'name': request.form["device_name"],
        'building_name': request.form["building_name"],
        'user_id': session["user_id"]
    })
    mongo.db.notifications.delete_many({
        'device': request.form["device_name"],
        'user_id': session["user_id"]
    })
    mongo.db.temperatures.delete_many({
        'username': session["username"],
        'device_name': request.form["device_name"]
    })
    mongo.db.humidity.delete_many({
        'username': session["username"],
        'device_name': request.form["device_name"]
    })

    return "success"
