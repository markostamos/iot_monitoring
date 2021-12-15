import paho.mqtt.client as paho
from random import randint
import CONFIG
import json
import time
import datetime


class Publisher():
    def __init__(self):

        self.client = paho.Client("publisher")

        self.client.on_publish = self.on_publish

    def connect(self, broker, port):
        self.client.connect(broker, port)

    def publish(self, topic, payload):
        json_payload = json.dumps(payload)
        self.client.publish(topic, payload=json_payload)

    def on_publish(self, client, userdata, result):
        print(f'Data published!')


if __name__ == "__main__":
    pub = Publisher()

    pub.connect(CONFIG.BROKER, CONFIG.PORT)
    topic = "sensors"

    while True:
        d = datetime.datetime.utcnow()
        for_js = int(time.mktime(d.timetuple())) * 1000
        payload = {
            "temperature": randint(-10, 40), "humidity": randint(0, 100), "timestamp": for_js}
        print(payload)
        pub.publish(topic, payload)
        time.sleep(2)
