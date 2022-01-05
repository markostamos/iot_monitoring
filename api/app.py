import eventlet
from flask import Flask
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
eventlet.monkey_patch()
from flask_pymongo import PyMongo
from config import Config
import json



app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)
mqtt = Mqtt(app)
socketio = SocketIO(app)
# bootstrap = Bootstrap(app)
# SETUP mongoDB


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


from routes import buildings, devices, main, users
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000,
                 use_reloader=False, debug=True)
