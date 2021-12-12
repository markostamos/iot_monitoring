topic = "sensors"
    payload = {"tmp": randint(-10, 40), "humidity": randint(0, 100)}
    pub.publish(topic, payload)