from __main__ import app, mongo
from utils.login_required import login_required
from flask import render_template, session, request
from bson import ObjectId


@app.route('/')
@app.route('/home')
def index():
    user = session.get('username')
    return render_template('index.html')


@app.route('/delete_notification', methods=["POST"])
@login_required
def delete_notification():
    """  mongo.db.notifications.delete_one({
         "user_id": session["user_id"],
         "_id": request.
     }) """
    print(request.form["notification_id"])

    mongo.db.notifications.delete_one({
        "user_id": session["user_id"],
        "_id": ObjectId(request.form["notification_id"])
    })
    return "success"


@app.route('/dashboard')
@login_required
def dashboard():
    devices = None
    buildings = list(mongo.db.buildings.find({
        "user_id": session["user_id"]
    }))
    chosen_building = request.args.get("chosen_building")
    chosen_device = request.args.get("chosen_device")
    if chosen_building:
        devices = list(mongo.db.devices.find({
            "user_id": session["user_id"],
            "building_name": chosen_building
        }))
    if chosen_building and chosen_device:
        notifications = list(mongo.db.notifications.find({
            "user_id": session["user_id"],
            "building": chosen_building,
            "device": chosen_device
        }))
    elif chosen_building:
        notifications = list(mongo.db.notifications.find({
            "user_id": session["user_id"],
            "building": chosen_building
        }))
    else:
        notifications = list(mongo.db.notifications.find({
            "user_id": session["user_id"]
        }))

    return render_template('dashboard.html', buildings=buildings, chosen_building=chosen_building, devices=devices, chosen_device=chosen_device, notifications=notifications)
