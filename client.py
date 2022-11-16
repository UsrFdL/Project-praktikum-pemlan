import paho.mqtt.client as mqtt
import random

class Pub():
    topic = "client"
    def __init__(self):
        self.mqttBroker ="mqtt.eclipseprojects.io"
    
    def connect(self):
        self.client = mqtt.Client(f"Toko-{random.randint(1, 999)}")
        self.client.connect(self.mqttBroker)

    def pub(self):
        numb = input()
        self.client.publish(Pub.topic, numb)
        print(f"publish {numb}")

    def run(self):
        self.connect()
        while True:
            self.pub()

class Sub(Pub):
    topic = "server"
    def __init__(self):
        self.mqttBroker = "mqtt.eclipseprojects.io"

    def connect(self):
        self.client = mqtt.Client(f"Toko-{random.randint(1, 999)}")
        self.client.connect(self.mqttBroker)

    def subscribe(self):
        def on_message(client, userdata, message):
            print("received message:" ,str(message.payload.decode("utf-8")))
        self.client.subscribe(self.topic)
        self.client.on_message = on_message

    def run(self):
        self.connect()
        self.client.loop_start()
        self.subscribe()
        while True:
            self.pub()
        # self.client.loop_forever()


if __name__ == "__main__":
    publ = Pub()
    publ.connect()
    subs = Sub()
    subs.run()