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

    def menu(self):
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

    def menu_login(self, msg):
        if msg[1]:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                lis = ["Tarik tunai", "Deposit", "Transfer", "Info ATM", "Keluar"]
                for i in range(0, len(lis)):
                    print(f"{f'{i+1}.': <25}{lis[i]: >10}")
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

    def menu_register(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        nama = input("Masukkan nama lengkap anda:\n:> ")
        os.system('cls' if os.name == 'nt' else 'clear')
        pin = input("Masukkan PIN:\n:> ")

        return nama, pin
        
    def tarik_tunai(self, msg):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Tarik tunai\n\n{'saldo:': <25}{msg[3]: >10}")
        cek = False
        uang = 0
        pin = 0
        try:
            tarikTunai = int(input(f"{'Jumlah tarik tunai:': <16}{'': >10}"))
        except ValueError:
            print("Masukan harus angka")
        else:            
            if tarikTunai > int(msg[3]):
                print("Saldo tidak mencukupi")
            elif tarikTunai <= 0:
                print("Uang tidak boleh kurang dari 0")
            elif tarikTunai < 10000:
                print("Minimal tarik tunai 10.000")
            else:
                cek = True
                uang = tarikTunai
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    try:
                        pin = int(input(f"{'Masukkan pin anda:': <16}{'': >10}"))
                    except ValueError:
                        print("Pin harus angka")
                    else:
                        if pin < 0:
                            print("Pin harus bilangan positif")
                        elif len(str(pin)) != 4:
                            print("Pin berjumlah 4 digit")
                        else:
                            break
                    time.sleep(1)
                return cek, uang, pin
        time.sleep(2)
        return cek, uang, pin

    def deposit(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Deposit\n")
        cek = False
        uang = 0
        pin = 0
        try:
            depo = int(input(f"{'Masukkan uang tunai:': <16}{'': >10}"))
        except ValueError:            
            print("Masukan harus angka")
        else:
            if depo <= 0:
                print("Uang tidak boleh kurang dari 0")
            elif depo < 10000:
                print("Minimal tarik tunai 10.000")
            else:
                cek = True
                uang = depo
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    try:
                        pin = int(input(f"{'Masukkan pin anda:': <16}{'': >10}"))
                    except ValueError:
                        print("Pin harus angka")
                    else:
                        if pin < 0:
                            print("Pin harus bilangan positif")
                        elif len(str(pin)) != 4:
                            print("Pin berjumlah 4 digit")
                        else:
                            break
                    time.sleep(1)
                return cek, uang, pin
        time.sleep(2)
        return cek, uang, pin
    
    #Belum selesai
    def transfer(self, msg):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Transfer\n")
        cek = False
        uang = 0
        pin = 0
        try:
            tujuan = int(input(f"{'Masukkan rekening tujuan:': <16}{'': >10}"))
        except ValueError:            
            print("Masukan harus angka")
        else:
            if tujuan < 0:
                print("rekening harus bilangan positif")
            elif len(str(tujuan)) != 5:
                print("rekening berjumlah 5 digit")
            else:
                cek = True
                uang = depo
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    try:
                        pin = int(input(f"{'Masukkan pin anda:': <16}{'': >10}"))
                    except ValueError:
                        print("Pin harus angka")
                    else:
                        if pin < 0:
                            print("Pin harus bilangan positif")
                        elif len(str(pin)) != 4:
                            print("Pin berjumlah 4 digit")
                        else:
                            break
                    time.sleep(1)
                return cek, uang, pin
        time.sleep(2)
        return cek, uang, pin

    def dashboard(self, msg=["home"]):
        if msg[0] == "home":
            pilih = self.menu()
            if pilih == 1:
                return f"login,{self.input_pw_pass()}"
            elif pilih == 2:
                return f"register,{self.input_pw_pass()}"
        elif msg[0] == "register":
            if eval(msg[1]):
                nama, pin = self.menu_register()
                return f"register_2,{nama},{pin}"
            else:
                print("Username sudah digunakan")
                time.sleep(2)
                return self.dashboard()
        elif msg[0] == "register_2":
            if eval(msg[1]):
                print("Akun berhasil dibuat")
                time.sleep(2)
                return self.dashboard()
        elif msg[0] == "login":
            if eval(msg[1]):
                pilih = self.menu_login(msg)
                if pilih == 1:
                    cek, uang, pin = self.tarik_tunai(msg)
                    if cek:
                        return f"tarik_tunai,{msg[2]},{uang},{pin}"
                elif pilih == 2:
                    cek, uang, pin = self.deposit()
                    if cek:
                        return f"deposit,{msg[2]},{uang},{pin}"
                elif pilih == 5:
                    return self.dashboard()
            else:
                print("Username atau password salah")
                time.sleep(2)
                return self.dashboard()
        elif msg[0] == "tarik_tunai" or msg[0] == "deposit":
            print(msg[4])
            time.sleep(2)
            msg[0] = "login"
            return self.dashboard(msg)

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

    def request(self, msg=["home"]):
        self.publish(self.dashboard(msg))

    def subscribe(self):
        def on_message(client, userdata, message):
            # print("received message:" ,message.payload.decode("utf-8"))
            self.request(list(message.payload.decode("utf-8").split(",")))
        self.client.subscribe(self.topicServer)
        self.client.on_message = on_message

    def run(self):
        self.connect()
        # self.client.loop_start()
        self.subscribe()
        self.request()
        self.client.loop_forever()


if __name__ == "__main__":
    user = Client()
    user.run()
    