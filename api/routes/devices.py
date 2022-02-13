
from __main__ import app, mqtt, mongo
from flask import session, render_template, request, redirect, url_for
from utils.login_required import login_required


@app.route('/<building_name>/devices')
@login_required
def building_devices(building_name):
    session["building_name"] = building_name
    devices = list(mongo.db.devices.find(
        {'building_name': building_name,
         'user_id': session["user_id"]
         }))
    """ session["path"] = f'{session["username"]}/{session["building_name"]}' """
    session["path"] = [session['username'], session["building_name"]]
    return render_template('devices.html', devices=devices, buildings=None)


@app.route('/new_device', methods=["POST"])
@app.route('/<building_name>/new_device', methods=["POST"])
@login_required
def new_device():
    mongo.db.devices.insert_one({
        'name': request.form['name'],
        'type': request.form['type'],
        'building_name': request.args.get("building_name") if request.args.get("building_name") else request.form["building_name"],
        'user_id': session['user_id']
    })
    if request.args.get("building_name"):
        return redirect(url_for('building_devices', building_name=request.args.get("building_name")))
    else:
        return redirect(url_for("all_devices"))


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

    mongo.db.devices.delete_one({
        'name': request.form["device_name"],
        'user_id': session["user_id"]
    })

    return "Success"


@app.route('/all_devices')
@login_required
def all_devices():
    devices = list(mongo.db.devices.find(
        {'user_id': session["user_id"]}))
    buildings = list(mongo.db.buildings.find(
        {'user_id': session["user_id"]}))
    session["path"] = [session["username"], "Devices"]
    return render_template('devices.html', devices=devices, buildings=buildings)
