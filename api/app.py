
import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_pymongo import PyMongo

eventlet.monkey_patch()

app = Flask(__name__)

# MQTT CONFIG
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 50
app.config['MQTT_TLS_ENABLED'] = False

# MONGODB CONFIG
app.config['SECRET_KEY'] = "mysecretkey"
app.config['MONGO_URI'] = "mongodb+srv://markosaris:markosaris@cluster0.rmljq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# SETUP mongoDB
mongodb_client = PyMongo(app)
db = mongodb_client.db


# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
socketio = SocketIO(app)
# bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


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


@ mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


@ mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('sensors')
    print("connected")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000,
                 use_reloader=False, debug=True)
