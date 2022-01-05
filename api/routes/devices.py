
from __main__ import app,mqtt
from flask import session,render_template
from utils.login_required import login_required



@app.route('/sensor/<device_id>/<device_name>')
@login_required
def sensor(device_id,device_name):
    mqtt.unsubscribe_all()
    mqtt.subscribe('sensors')
    session["device_id"] = device_id
    session["device_name"] = device_name
    
    return render_template('sensor.html')
