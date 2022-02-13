
from __main__ import app, mqtt, mongo
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


@app.route('/<building_name>/<device_name>/')
@login_required
def sensor(building_name, device_name):
    device = mongo.db.devices.find_one(
        {'building_name': building_name,
         'user_id': session["user_id"]
         })

    """ mqtt.unsubscribe_all()
    mqtt.subscribe(device["password"]) """

    return render_template('sensor.html')


@app.route('/device/<_name>/<_type>/<building>')
@login_required
def get_device(_name, _type, building):

    session["device_name"] = _name
    session["building_name"] = building
    """ session["path"] = f'{session["username"]}/{session["building_name"]}/{session["device_name"]}' """
    session["path"] = [session['username'],
                       session["building_name"], session["device_name"]]
    if _type == "sensor":
        return redirect(url_for('sensor', building_name=building, device_name=session["device_name"]))

    else:
        print('TODO')


@app.route('/delete_device', methods=["POST"])
@login_required
def delete_device():
    print("CALLED")
    mongo.db.devices.delete_one({
        'name': request.form["device_name"],
        'building_name': request.form["building_name"],
        'user_id': session["user_id"]
    })
    mongo.db.notifications.delete_many({
        'device': request.form["device_name"],
        'user_id': session["user_id"]
    })

    return "success"
