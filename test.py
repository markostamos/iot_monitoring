import paho.mqtt.client as paho
from random import randint
import CONFIG
import json
from time import sleep


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

        payload = {"tmp": randint(-10, 40), "humidity": randint(0, 100)}
        print(payload)
        pub.publish(topic, payload)
        sleep(1)
#asasasa
