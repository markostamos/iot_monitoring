import paho.mqtt.client as mqtt
import datetime
import time
from pymongo import MongoClient
from gpiozero import MotionSensor
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(11,GPIO.OUT)
#GPIO.setup(12,GPIO.OUT)
servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz
#servo2 = GPIO.PWM(12,50)
# Start PWM running, with value of 0 (pulse off)
servo1.start(0)
#servo2.start(0)

# pir = MotionSensor(4)


MQTT_ADDRESS = '192.168.1.13'
MQTT_USER = 'aris'
MQTT_PASSWORD = 'aris'
MQTT_TOPIC = 'farm/+'

mongoClient=MongoClient("mongodb+srv://markosaris:markosaris@cluster0.rmljq.mongodb.net/farmers_buddy_db?retryWrites=true&w=majority")
db=mongoClient.farmers_buddy_db
collection=db.devices


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    message=msg.payload.decode("utf-8")
    timestamp = int(time.mktime(time.localtime()))
    print(msg.topic + ' ' + str(msg.payload))
    if (msg.topic == "farm/humidity"):
        collection=db.humidity
    elif (msg.topic == "farm/temperatures"): 
        collection=db.temperatures
    else :
        collection=db.devices
    
    post={"timestamp":timestamp,"value":message,"username":"Aris","device_name":"gisdakis"}
    collection.insert_one(post)

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()
#   while True:
#	    pir.wait_for_motion()
#	    angle1 = float()
#       angle2 = float()
#       servo1.ChangeDutyCycle(2+(angle1/18))
#       time.sleep(0.5)
#       servo2.ChangeDutyCycle(2+(angle2/18))
#       time.sleep(0.5)
#
#	    pir.wait_for_no_motion()
#       servo1.ChangeDutyCycle(0)
#       servo2.ChangeDutyCycle(0)

if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
