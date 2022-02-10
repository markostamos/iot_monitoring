from __main__ import app, mongo
from utils.login_required import login_required
from flask import render_template, session, url_for, request, redirect


@app.route('/buildings')
@login_required
def buildings():
    buildings = list(mongo.db.buildings.find(
        {'user_id': session['user_id']}))
    """ session["path"] = f'{session["username"]}/' """
    session["path"] = [session['username']]
    return render_template('buildings.html', buildings=buildings)


""" 
@app.route('/buildings/<_id>/<_name>/')
@login_required
def get_devices(_id, _name):


    return redirect(url_for('building_devices', building=_name.replace(" ", "_")))
 """


@app.route('/buildings/new_building', methods=["POST"])
@login_required
def new_building():

    mongo.db.buildings.insert_one({
        'name': request.form['name'],
        'location': request.form['location'],
        'user_id': session['user_id']
    })

    return redirect(url_for('buildings'))


@app.route('/delete_building/<building_name>')
@login_required
def delete_building(building_name):

    mongo.db.buildings.delete_one({
        'name': building_name,
        'user_id': session["user_id"]
    })

    newvalues = {"$set": {"building_name": ""}}

    mongo.db.devices.update_many(
        {
            'user_id': session['user_id'],
            'building_name': building_name
        },
        {
            "$set": {"building_name": ""}
        }
    )

    return redirect(url_for('buildings'))
