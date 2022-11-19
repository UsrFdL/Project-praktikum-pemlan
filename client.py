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

    def menu_utama(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("1.Login\n2.Register")
            try:
                masukan = int(input("Masukan Pilihan Anda: "))
                if masukan == 1 and masukan == 2:
                    break
                else:
                    print("masukkan angka 1 atau 2")
            except ValueError:
                print("Masukkan angka")
            time.sleep(2)
            
        return masukan 

    def login(self, msg):
        if msg[1]:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"{'1.': <15}{'Tarik tunai': >15}")
                print(f"{'2.': <15}{'Deposit': >15}\n")
                print(f"{'3.': <15}{'Transfer': >15}\n")
                print(f"{'4.': <15}{'Info ATM': >15}\n")
                print(f"{'saldo': <15}{msg[2]: >15}")
                try:
                    masukan = int(input(":> "))
                    if masukan == 1 and masukan == 2:
                        break
                    else:
                        print("Pilih angka 1 hingga 4")
                except ValueError:
                    print("Harus memasukkan angka")
                time.sleep(2)
            
            return masukan

    def tarik_tunai(self, msg):
        while True:
            tarikTunai = int(input(f"{'Jumlah tarik tunai': <15}{'': >15}"))
            if tarikTunai > msg[1]:
                print("Saldo tidak mencukupi")
                time.sleep(2)
            elif tarikTunai < 0:
                print("Uang tidak boleh kurang dari 0")
                time.sleep(2)
            elif tarikTunai < 10000:
                print("Minimal tarik tunai 10.000")
                time.sleep(2)
            else:
                break
        
        return tarikTunai


            

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
            if self.menu_utama() == 1:
                self.publish(f"login,{self.input_pw_pass()}")
            elif self.menu_utama() == 2:
                self.publish(f"register,{self.input_pw_pass()}")
        elif msg[0] == "register":
            msg[1]
        elif msg[0] == "login":
            if eval(msg[1]):
                if self.login(msg) == 1:
                    self.publish(f"tarik_tunai,{self.tarik_tunai(msg)},{msg[2]}")

                
    
    def subscribe(self):
        def on_message(client, userdata, message):
            print("received message:" ,message.payload.decode("utf-8"))
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
    