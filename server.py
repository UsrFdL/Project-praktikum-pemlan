import paho.mqtt.client as mqtt
import random
import os
import csv

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
            print("received message:" ,message.payload.decode("utf-8"))
            self.publish(message.payload.decode("utf-8"))
            msg = list(message.payload.decode("utf-8").split(","))
            if(msg[0] == "register"):
                self.publish(self.register(msg[1], msg[2]))
        self.client.subscribe(self.topicClient)
        self.client.on_message = on_message

    def run(self):
        self.connect()
        self.subscribe()
        self.client.loop_forever()

class dataBase(Server):
    def __init__(self):
        super().__init__()
        self.fieldname = ["username", "password", "nama", "pin", "rekening", "uang", "mutasi"]
        if not os.path.exists("account.csv"):
            with open("account.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldname)
                writer.writeheader()               

    def register(self, username, password):
        ganda = False
        with open("account.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if username == row["username"]:
                    ganda = True
        
        if not ganda:
            with open("user.csv", "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldname)
                writer.writerow({"username":username, "password": password})
            return True
        else:
            return False

class runServer(dataBase):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    backEnd = runServer()
    backEnd.run()