import paho.mqtt.client as mqtt
import random
import os
import csv
import pandas

class dataBase():
    def __init__(self):
        self.fieldname = ["username", "password", "nama", "pin", "rekening", "saldo", "mutasi"]
        if not os.path.exists("account.csv"):
            with open("account.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldname)
                writer.writeheader()
        self.tmpRow = []

    def register(self, username, password):
        ganda = False
        with open("account.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if username == row["username"]:
                    ganda = True

        if not ganda:
            # with open("account.csv", "a", newline="") as file:
            #     writer = csv.DictWriter(file, fieldnames=self.fieldname)
            #     writer.writerow({"username":username, "password": password})
            self.tmpRow.append(username)
            self.tmpRow.append(password)
            return True
        else:
            return False

    def login(self, username, password):
        with open("account.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if username == row["username"] and password == row["password"]:
                    return f"{True},{row['rekening']},{row['saldo']}"
                else:
                    return False

    def depo_tarikTunai(self, msg):
        with open("account.csv", "r") as file:
            reader = csv.DictReader(file)
            idx = 0
            for row in reader:
                if msg[1] == row["rekening"]:
                    if msg[0] == "tarik_tunai":
                        total = int(row["saldo"]) - int(msg[2])
                    elif msg[0] == "deposit":
                        total = int(row["saldo"]) + int(msg[2])
                    pd = pandas.read_csv("account.csv")
                    pd.loc[idx, "saldo"] = total
                    pd.to_csv("account.csv")
                    return f"{True},{msg[1]},{total},Berhasil tarik tunai {msg[2]}"
                idx += 1
            return False

class Server(dataBase):
    def __init__(self):
        super().__init__()
        self.mqttBroker ="mqtt.eclipseprojects.io"
        self.topicClient = "client"
        self.topicServer = "server"

    def connect(self):
        self.client = mqtt.Client(f"Server-{random.randint(1, 999)}")
        self.client.connect(self.mqttBroker)

    def publish(self, data):
        self.client.publish(self.topicServer, data)
        print(f"publish {data} dengan topic {self.topicServer}")

    def response(self, msg):
        msg = list(msg.split(","))
        if msg[0] == "register":
            self.publish(f"register,{self.register(msg[1], msg[2])}")
        elif msg[0] == "login":
            self.publish(f"login,{self.login(msg[1], msg[2])}")
        elif msg[0] == "tarik_tunai":
            self.publish(f"tarik_tunai,{self.depo_tarikTunai(msg)}")
        elif msg[0] == "deposit":
            self.publish(f"deposit,{self.depo_tarikTunai(msg)}")
        
    def subscribe(self):
        def on_message(client, userdata, message):
            print("received message:" ,message.payload.decode("utf-8"))
            # self.publish(message.payload.decode("utf-8"))
            self.response(message.payload.decode("utf-8"))

        self.client.subscribe(self.topicClient)
        self.client.on_message = on_message

    def run(self):
        self.connect()
        self.subscribe()
        self.client.loop_forever()

if __name__ == "__main__":
    backEnd = Server()
    backEnd.run()