import os


class Config:
    SECRET_KEY = 'my secret'
    SECRET = 'my secret key'
    TEMPLATES_AUTO_RELOAD = True
    MQTT_BROKER_URL = 'broker.hivemq.com'
    MQTT_BROKER_PORT = 1883
    MQTT_USERNAME = ''
    MQTT_PASSWORD = ''
    MQTT_KEEPALIVE = 50
    MQTT_TLS_ENABLED = False
    MONGO_URI = "mongodb+srv://markosaris:markosaris@cluster0.rmljq.mongodb.net/farmers_buddy_db?retryWrites=true&w=majority"