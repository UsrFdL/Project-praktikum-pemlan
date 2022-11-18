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

    def menu_login(self):
        username = input("Username")
        password = input("Password")
        return f"{username},{password}"

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
    
    def subscribe(self):
        def on_message(client, userdata, message):
            print("received message:" ,message.payload.decode("utf-8"))
        self.client.subscribe(self.topicServer)
        self.client.on_message = on_message

    def dashboard(self):
        while True:
            if self.menu_utama() == 1:
                self.publish(f"login,{self.menu_login()}")

                

    def run(self):
        self.connect()
        self.client.loop_start()
        self.subscribe()
        self.dashboard()



if __name__ == "__main__":
    user = Client()
    user.run()
    