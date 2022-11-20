import paho.mqtt.client as mqtt
import random
import os
import time

class ATM():
    def __init__(self):
        pass

    def input_pw_pass(self):
        username = input("Username: ")
        password = input("Password: ")
        return f"{username},{password}"

    def login(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("1.Login\n2.Register")
            try:
                masukan = int(input("Masukan Pilihan Anda: "))
                if masukan >= 1 and masukan <= 2:
                    break
                else:
                    print("masukkan angka 1 atau 2")
            except ValueError:
                print("Masukan harus angka")
            time.sleep(2)

        return masukan 

    def menu_utama(self, msg):
        if msg[1]:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                lis = ["Tarik tunai", "Deposit", "Transfer", "Info ATM", "Keluar"]
                for i in range(0, len(lis)):
                    print(f"{f'{i+1}.': <25}{lis[i]: >10}")
                # print(f"{'1.': <25}{'Tarik tunai': >10}")
                # print(f"{'2.': <25}{'Deposit': >10}")
                # print(f"{'3.': <25}{'Transfer': >10}")
                # print(f"{'4.': <25}{'Info ATM': >10}")
                # print(f"{'5.': <25}{'Keluar': >10}\n")
                print(f"\n{'saldo:': <25}{msg[3]: >10}")
                try:
                    masukan = int(input(":> "))
                    if masukan >= 1 and masukan <= 5:
                        break
                    else:
                        print("Pilih angka 1 hingga 5")
                except ValueError:
                    print("Masukan harus angka")
                time.sleep(2)
            
            return masukan

    def tarik_tunai(self, msg):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Tarik tunai\n\n{'saldo:': <25}{msg[3]: >10}")
        cek = False
        uang = 0
        try:
            tarikTunai = int(input(f"{'Jumlah tarik tunai:': <16}{'': >10}"))
            if tarikTunai > int(msg[3]):
                print("Saldo tidak mencukupi")
            elif tarikTunai <= 0:
                print("Uang tidak boleh kurang dari 0")
            elif tarikTunai < 10000:
                print("Minimal tarik tunai 10.000")
            else:
                cek = True
                uang = tarikTunai
                return cek, uang
        except ValueError:
            print("Masukan harus angka")
        time.sleep(2)        
        return cek, uang

    def deposit(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Deposit\n")
        cek = False
        uang = 0
        try:
            depo = int(input(f"{'Masukkan uang tunai:': <16}{'': >10}"))
            if depo <= 0:
                print("Uang tidak boleh kurang dari 0")
            elif depo < 10000:
                print("Minimal tarik tunai 10.000")
            else:
                cek = True
                uang = depo
                return cek, uang
        except ValueError:            
            print("Masukan harus angka")
        time.sleep(2)
        return cek, uang

class Client(ATM):
    def __init__(self):
        self.mqttBroker ="mqtt.eclipseprojects.io"
        self.topicClient = "client"
        self.topicServer = "server"

    def connect(self):
        self.client = mqtt.Client(f"Server-{random.randint(1, 999)}")
        self.client.connect(self.mqttBroker)

    def publish(self, teks):
        self.client.publish(self.topicClient, teks)
        print(f"publish {teks} dengan topic {self.topicClient}")

    def dashboard(self, msg=["home"]):
        if msg[0] == "home":
            pilih = self.login()
            if pilih == 1:
                self.publish(f"login,{self.input_pw_pass()}")
            elif pilih() == 2:
                self.publish(f"register,{self.input_pw_pass()}")
        elif msg[0] == "register":
            msg[1]
        elif msg[0] == "login":
            if eval(msg[1]):
                pilih = self.menu_utama(msg)
                if pilih == 1:
                    cek, uang = self.tarik_tunai(msg)
                    if cek:
                        self.publish(f"tarik_tunai,{msg[2]},{uang}")
                elif pilih == 2:
                    cek, uang = self.deposit()
                    if cek:
                        self.publish(f"deposit,{msg[2]},{uang}")
                elif pilih == 5:
                    self.dashboard()
            else:
                print("Username atau password salah")
                time.sleep(2)
                self.dashboard()
        elif msg[0] == "tarik_tunai" or msg[0] == "deposit":
            if eval(msg[1]):
                print(msg[4])
                time.sleep(2)
                msg[0] = "login"
                self.dashboard(msg)

    def subscribe(self):
        def on_message(client, userdata, message):
            # print("received message:" ,message.payload.decode("utf-8"))
            self.dashboard(list(message.payload.decode("utf-8").split(",")))
        self.client.subscribe(self.topicServer)
        self.client.on_message = on_message


    def run(self):
        self.connect()
        # self.client.loop_start()
        self.subscribe()
        self.dashboard()
        self.client.loop_forever()


if __name__ == "__main__":
    user = Client()
    user.run()
    