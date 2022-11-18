import paho.mqtt.client as mqtt
import random

class Dashboard():
    def __init__(self):
        super().__init__()
        print("1.Login\n2.Register")
        masukan = input(int("Masukan Pilihan Anda: "))
        if masukan == 1:
            self.login()

    def login(self):
        username = input("Username")
        password = input("Password")

class Client(Dashboard):
    def __init__(self):
        self.mqttBroker ="mqtt.eclipseprojects.io"
        self.topicClient = "client"
        self.topicServer = "server"

    def connect(self):
        self.client = mqtt.Client(f"Server-{random.randint(1, 999)}")
        self.client.connect(self.mqttBroker)

    def publish(self):
        numb = input()
        self.client.publish(self.topicClient, numb)
        print(f"publish {numb} dengan topic {self.topicClient}")
    
    def subscribe(self):
        def on_message(client, userdata, message):
            print("received message:" ,message.payload.decode("utf-8"))
        self.client.subscribe(self.topicServer)
        self.client.on_message = on_message

    def run(self):
        self.connect()
        self.client.loop_start()
        self.subscribe()
        while True:
            self.publish()

if __name__ == "__main__":
    user = Client()
    user.run()
    