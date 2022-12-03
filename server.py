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

    def register(self, username, password):
        ganda = False
        with open("account.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if username == row["username"]:
                    ganda = True

        if not ganda:
            return f"{True},{username},{password}"
        else:
            return f"{False}"
        
    def register_2(self, nama, pin, username, password):
        awal = list("00000")
        tmp = str(random.randrange(1, 99999))
        for i in range(5):
            if i >= 5 - len(tmp):
                awal[i] = tmp[i - (5 - len(tmp))]
        rekening = "".join(awal)
        
        with open("account.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldname)
            writer.writerow({"username":username, "password":password, "nama":nama, "pin":pin, "rekening":rekening, "saldo":0, "mutasi":"kosong"})

        return True

    def login(self, username, password):
        with open("account.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if username == row["username"] and password == row["password"]:
                    return f"{True},{row['rekening']},{row['saldo']}"
            return False

    def depo_tarikTunai(self, msg):
        pd = pandas.read_csv("account.csv")
        with open("account.csv", "r") as file:
            reader = csv.DictReader(file)
            idx = saldo_awal = saldo = 0
            pesan = ""
            for row in reader:
                if msg[2] == row["rekening"]:
                    saldo_awal = row["saldo"]
                    if msg[4] != row["pin"]:
                        return f"{True},{msg[2]},{saldo_awal},Pin salah"
                    elif msg[1] == "tarik_tunai":
                        saldo = int(saldo_awal) - int(msg[3])
                        pesan = "tarika tunai"
                    elif msg[1] == "deposit":
                        saldo = int(saldo_awal) + int(msg[3])
                        pesan = "deposit"
                    pd.loc[idx, "saldo"] = saldo
                    if row["mutasi"] == "kosong":
                        pd.loc[idx, "mutasi"] = f"{pesan.capitalize()} | {msg[5]} | {msg[3]}"
                    else:
                        mutasi = row["mutasi"]+f"&{pesan.capitalize()} | {msg[5]} | {msg[3]}"
                        pd.loc[idx, "mutasi"] = mutasi
                    pd.to_csv("account.csv", index=False)
                    return f"{True},{msg[2]},{saldo},Berhasil {pesan} senilai {msg[3]}"
                idx += 1

    def transfer(self, msg):
        idx = saldo_pengirim = idx_pengirim = saldo_penerima = idx_penerima= 0
        cek_rek = False
        pd = pandas.read_csv("account.csv")
        with open("account.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if msg[2] == row["rekening"]:
                    saldo_pengirim = row["saldo"]
                    cek_pin = True if msg[5] == row["pin"] else False
                    idx_pengirim = idx
                if msg[3] == row["rekening"]:
                    saldo_penerima = row["saldo"]
                    idx_penerima = idx
                    nama_penerima = row["nama"]
                    cek_rek = True
                idx += 1
        if not cek_rek:
            return f"{True},{msg[2]},{saldo_pengirim},Nomor rekening tujuan tidak ditemukan"
        if cek_pin:
            saldo_pengirim = int(saldo_pengirim) - int(msg[4])
            saldo_penerima = int(saldo_penerima) + int(msg[4])
            pd.loc[idx_pengirim, "saldo"] = saldo_pengirim
            if pd.at[idx_pengirim, "mutasi"] == "kosong":
                pd.loc[idx_pengirim, "mutasi"] = f"Transfer | {msg[6]} | -{msg[4]}"
            else:
                mutasi = pd.at[idx_pengirim, "mutasi"]+f"&Transfer | {msg[6]} | -{msg[4]}"
                pd.loc[idx_pengirim, "mutasi"] = mutasi
            pd.loc[idx_penerima, "saldo"] = saldo_penerima
            if pd.at[idx_penerima, "mutasi"] == "kosong":
                pd.loc[idx_penerima, "mutasi"] = f"Transfer | {msg[6]} | +{msg[4]}"
            else:
                mutasi = pd.at[idx_penerima, "mutasi"]+f"&Transfer | {msg[6]} | +{msg[4]}"
                pd.loc[idx_penerima, "mutasi"] = mutasi
            pd.to_csv("account.csv", index=False)
            return f"{True},{msg[2]},{saldo_pengirim},Berhasil transfer ke {nama_penerima} sebesar {msg[4]}"
        else:
            return f"{True},{msg[2]},{saldo_pengirim},Pin yang anda masukkan salah"
           
    def info(self, rekening):
        with open("account.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if rekening == row["rekening"]:
                    return f"{True},{rekening},{row['saldo']},{row['nama']},{row['mutasi']},"

    def operasi(self, msg):
        if msg[1] == "register":
            return f"register,{self.register(msg[2], msg[3])}"
        elif msg[1] == "register_2":
            return f"register_2,{self.register_2(msg[2], msg[3], msg[4], msg[5])}"
        elif msg[1] == "login":
            return f"login,{self.login(msg[2], msg[3])}"
        elif msg[1] == "tarik_tunai":
            return f"tarik_tunai,{self.depo_tarikTunai(msg)}"
        elif msg[1] == "deposit":
            return f"deposit,{self.depo_tarikTunai(msg)}"
        elif msg[1] == "transfer":
            return f"transfer,{self.transfer(msg)}"
        elif msg[1] == "info":
            return f"info,{self.info(msg[2])}"

                
class Server(dataBase):
    def __init__(self):
        super().__init__()
        self.mqttBroker ="mqtt.eclipseprojects.io"
        self.topicClient = "client"
        self.topicServer = ""

    def connect(self):
        self.client = mqtt.Client(f"Server-{random.randint(1, 999)}")
        self.client.connect(self.mqttBroker)

    def publish(self, data):
        self.client.publish(self.topicServer, data)
        print(f"publish {data} dengan topic {self.topicServer}")

    def response(self, msg):
        self.topicServer = msg[0]
        self.publish(self.operasi(msg))
        
    def subscribe(self):
        def on_message(client, userdata, message):
            print("received message:" ,message.payload.decode("utf-8"))
            self.response(list(message.payload.decode("utf-8").split(",")))
        self.client.subscribe(self.topicClient)
        self.client.on_message = on_message

    def run(self):
        self.connect()
        self.subscribe()
        self.client.loop_forever()

if __name__ == "__main__":
    backEnd = Server()
    backEnd.run()