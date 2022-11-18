import paho.mqtt.client as mqtt
import random

class ATM():
    def __init__(self):
        pass

    def menu_utama(self):
        print("1.Login\n2.Register")
        while True:
            try:
                masukan = int(input("Masukan Pilihan Anda: "))
                if masukan != 1 and masukan != 2:
                    print("masukkan angka 1 atau 2")
                else:
                    break
            except ValueError:
                print("Masukkan angka")
            
        return masukan 

    def input_pw_pass(self):
        username = input("Username: ")
        password = input("Password: ")
        return f"{username},{password}"

    def login(self, msg):
        if msg[1]:
            print(f"selamat datang {msg[2]}")

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

    def get(self, bool):
        msg = list(bool.split(","))
        if msg[0] == "login":
            if eval(msg[1]):
                print("Masuk")
        elif msg[0] == "register":
            if eval(msg[1]):
                print("Berhasil")
        else:
            self.menu_utama()

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
                self.login(msg)

    
    def subscribe(self):
        def on_message(client, userdata, message):
            print("received message:" ,message.payload.decode("utf-8"))
            self.dashboard(list(message.payload.decode("utf-8").split(",")))
        self.client.subscribe(self.topicServer)
        self.client.on_message = on_message


    def run(self):
        self.connect()
        self.client.loop_start()
        self.subscribe()
        self.dashboard()
        # self.client.loop_forever()


if __name__ == "__main__":
    user = Client()
    user.run()
    