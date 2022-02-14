from __main__ import app, mongo
from utils.login_required import login_required
from flask import render_template, session, request
from bson import ObjectId


@app.route('/')
@app.route('/home')
def index():

    return render_template('index.html')


@app.route('/delete_notification', methods=["POST"])
@login_required
def delete_notification():

    mongo.db.notifications.delete_one({
        "username": session["username"],
        "_id": ObjectId(request.form["notification_id"])
    })
    return "success"


@app.route('/delete_notifications', methods=["POST"])
@login_required
def delete_notifications():

    if request.form["device"] == "None" and request.form["building"] == "None":
        mongo.db.notifications.delete_many({
            'username': session["username"]
        })
    elif request.form["device"] == "None":
        mongo.db.notifications.delete_many({
            'username': session["username"],
            'building': request.form["building"]
        })
    else:
        mongo.db.notifications.delete_many({
            'username': session["username"],
            'building': request.form["building"],
            'device': request.form["device"]
        })

    print(request.form["building"])
    return "success"


@app.route('/get_notifications', methods=["POST"])
@login_required
def get_notifications():

    if request.form["device"] == "None" and request.form["building"] == "None":
        notifications = list(mongo.db.notifications.find({
            'username': session["username"]
        }))
    elif request.form["device"] == "None":
        notifications = list(mongo.db.notifications.find({
            'username': session["username"],
            'building': request.form["building"]
        }))
    else:
        notifications = list(mongo.db.notifications.find({
            'username': session["username"],
            'building': request.form["building"],
            'device': request.form["device"]
        }))

    res = {
        "notifications": []
    }
    for notification in notifications:
        res["notifications"].append({
            "_id": str(notification["_id"]),
            "text": notification["text"],
            "date": str(notification["date"]),
            "building": notification["building"],
            "severity": notification["severity"],
            "device": notification["device"]

        })
    return res


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
            "username": session["username"],
            "building": chosen_building,
            "device": chosen_device
        }))
    elif chosen_building:
        notifications = list(mongo.db.notifications.find({
            "username": session["username"],
            "building": chosen_building
        }))
    else:
        notifications = list(mongo.db.notifications.find({
            "username": session["username"]
        }))

    return render_template('dashboard.html', buildings=buildings, chosen_building=chosen_building, devices=devices, chosen_device=chosen_device, notifications=notifications)


@app.route('/get_temp_data', methods=["POST"])
def get_temp_data():

    temps = list(mongo.db.temperatures.find({
        "username": session["username"],
        "device_name": request.form["device_name"],
        "timestamp": {
            "$gt": request.form.get('lower_bound', type=int),
            "$lt": request.form.get('upper_bound', type=int)
        }
    }))

    res = {
        "values": [],
        "timestamps": []
    }
    for doc in temps:
        res["values"].append(doc["value"])
        res["timestamps"].append(int(doc["timestamp"]))

    return res


@app.route('/get_humidity_data', methods=["POST"])
def get_humidity_data():
    temps = list(mongo.db.humidity.find({
        "username": session["username"],
        "device_name": request.form["device_name"],
        "timestamp": {
            "$gt": request.form.get('lower_bound', type=int),
            "$lt": request.form.get('upper_bound', type=int)
        }
    }))
    res = {
        "values": [],
        "timestamps": []
    }
    for doc in temps:
        res["values"].append(doc["value"])
        res["timestamps"].append(int(doc["timestamp"]))

    return res


@app.route('/delete_data', methods=["POST"])
@login_required
def delete_data():
    if request.form["type"] == "ALL":
        mongo.db.temperatures.delete_many({
            "username": session["username"],
            "device_name": request.form["device_name"],
            "timestamp": {
                "$gt": request.form.get('lower_bound', type=int),
                "$lt": request.form.get('upper_bound', type=int)
            }
        })
        mongo.db.humidity.delete_many({
            "username": session["username"],
            "device_name": request.form["device_name"],
            "timestamp": {
                "$gt": request.form.get('lower_bound', type=int),
                "$lt": request.form.get('upper_bound', type=int)
            }
        })

        return "success"
    elif request.form["type"] == "temp":
        mongo.db.temperatures.delete_many({
            "username": session["username"],
            "device_name": request.form["device_name"],
            "timestamp": {
                "$gt": request.form.get('lower_bound', type=int),
                "$lt": request.form.get('upper_bound', type=int)
            }
        })
        return "success"
    elif request.form["type"] == "humidity":
        mongo.db.humidity.delete_many({
            "username": session["username"],
            "device_name": request.form["device_name"],
            "timestamp": {
                "$gt": request.form.get('lower_bound', type=int),
                "$lt": request.form.get('upper_bound', type=int)
            }
        })
        return "sucess"
    return "bad"
