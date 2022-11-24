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
            self.tmpRow.clear()
            self.tmpRow.append(username)
            self.tmpRow.append(password)
            return True
        else:
            return False
        
    def register_2(self, nama, pin):
        awal = list("00000")
        tmp = str(random.randrange(1, 99999))
        for i in range(5):
            if i >= 5 - len(tmp):
                awal[i] = tmp[i - (5 - len(tmp))]
        rekening = "".join(awal)
        
        with open("account.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldname)
            writer.writerow({"username":self.tmpRow[0], "password":self.tmpRow[1], "nama":nama, "pin":pin, "rekening":rekening, "saldo":0, "mutasi":"kosong"})

        return True

    def login(self, username, password):
        with open("account.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if username == row["username"] and password == row["password"]:
                    return f"{True},{row['rekening']},{row['saldo']}"
            return False

    def depo_tarikTunai(self, msg):
        with open("account.csv", "r") as file:
            reader = csv.DictReader(file)
            idx = 0
            saldo_asli = 0
            for row in reader:
                if msg[1] == row["rekening"]:
                    saldo_asli = row["saldo"]
                    if msg[3] != row["pin"]:
                        return f"{True},{msg[1]},{saldo_asli},Pin salah"
                    elif msg[0] == "tarik_tunai":
                        saldo = int(saldo_asli) - int(msg[2])
                        pesan = "tarika tunai"
                    elif msg[0] == "deposit":
                        saldo = int(saldo_asli) + int(msg[2])
                        pesan = "deposit"
                    pd = pandas.read_csv("account.csv")
                    pd.loc[idx, "saldo"] = saldo
                    pd.to_csv("account.csv", index=False)
                    return f"{True},{msg[1]},{saldo},Berhasil {pesan} senilai {msg[2]}"
                idx += 1

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
        elif msg[0] == "register_2":
            self.publish(f"register_2,{self.register_2(msg[1], msg[2])}")
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