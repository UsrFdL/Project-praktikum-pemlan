import paho.mqtt.client as mqtt
import random

class Server():
    def __init__(self):
        self.mqttBroker ="mqtt.eclipseprojects.io"
        self.topicClient = "client"
        self.topicServer = "server"

    def connect(self):
        self.client = mqtt.Client(f"Server-{random.randint(1, 999)}")
        self.client.connect(self.mqttBroker)

    def publish(self, data):
        self.client.publish(self.topicServer, data)
        print(f"publish {data} dengan topic {self.topicServer}")
    
    def subscribe(self):
        def on_message(client, userdata, message):
            print("received message:" ,str(message.payload.decode("utf-8")))
            self.publish(str(message.payload.decode("utf-8")))
        self.client.subscribe(self.topicClient)
        self.client.on_message = on_message

    def run(self):
        self.connect()
        self.subscribe()
        self.client.loop_forever()

""" class dataBase():
    def __init__(self):
        self. """

if __name__ == "__main__":
    backEnd = Server()

    backEnd.run()