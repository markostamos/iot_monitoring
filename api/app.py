import eventlet

import json
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
eventlet.monkey_patch()
from flask_pymongo import PyMongo
import bcrypt


from functools import wraps, update_wrapper


def login_required(func):
    # @wraps(func)
    def nei(*args, **kwargs):
        if session.get("username"):
            ret = func(*args, **kwargs)
            return ret
        else:
            return redirect(url_for('login'))
    update_wrapper(nei, func)
    return nei


app = Flask(__name__)

# MQTT CONFI
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 50
app.config['MQTT_TLS_ENABLED'] = False
app.secret_key = "DragonFire"
app.config["MONGO_URI"] = "mongodb+srv://markosaris:markosaris@cluster0.rmljq.mongodb.net/farmers_buddy_db?retryWrites=true&w=majority"

# MONGODB CONFIG

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'


mongo = PyMongo(app)


mqtt = Mqtt(app)
socketio = SocketIO(app)
# bootstrap = Bootstrap(app)
# SETUP mongoDB


@app.route('/')
@app.route('/home')
@login_required
def index():
    return render_template('layout.html')


@app.route('/sensor')
@login_required
def sensor():
    mqtt.subscribe('sensors')
    user = {"username": session["username"]}
    return render_template('sensor.html', username=session["username"])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/buildings')
@login_required
def buildings():
    return render_template('buildings.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        existing_user = mongo.db.users.find_one(
            {'email': request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())

            mongo.db.users.insert_one({
                'username': request.form['name'],
                'email': request.form['email'],
                'password': hashpass
            })
            session['username'] = request.form['name']
            return redirect(url_for('sensor'))

        return 'That email already exists!'

    return render_template('register.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})
        if login_user:

            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['username'] = login_user['username']
                session['user_id'] = str(login_user.get('_id'))
                return redirect(url_for('sensor'))
            else:
                return 'Invalid username/password combination'
    return render_template('login.html')


""" @socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message']) """


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=json.loads(message.payload.decode())
    )

    # print(f'message is {data["payload"]} ')
    socketio.emit('mqtt_message', data=data)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):

    print("connected")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000,
                 use_reloader=False, debug=True)
