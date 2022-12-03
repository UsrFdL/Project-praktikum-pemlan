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
                masukan = int(input("Masukkan Pilihan Anda: "))
                if masukan >= 1 and masukan <= 2:
                    break
                else:
                    print("Masukkan angka 1 atau 2")
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
        nama = input("Nama lengkap anda:\n:> ")
        os.system('cls' if os.name == 'nt' else 'clear')
        pin = input("PIN:\n:> ")
        return nama, pin
        
    def tarik_tunai(self, msg):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Tarik tunai\n\n{'saldo:': <25}{msg[3]: >10}")
        cek = False
        uang = pin = waktu = 0
        try:
            uang = int(input(f"{'Jumlah tarik tunai:': <16}{'': >10}"))
        except ValueError:
            print("Masukan harus angka")
        else:            
            if uang > int(msg[3]):
                print("Saldo tidak mencukupi")
            elif uang <= 0:
                print("Uang tidak boleh kurang dari 0")
            elif uang < 10000:
                print("Minimal tarik tunai 10.000")
            else:
                pin = input(f"{'Pin:': <20}{'': >10}")
                try:
                    int(pin)
                except ValueError:
                    print("Pin harus angka")
                else:
                    if int(pin) < 0:
                        print("Pin harus bilangan positif")
                    elif len(pin) != 4:
                        print("Pin berjumlah 4 digit")
                    else:
                        cek = True
                        waktu = time.strftime("%d/%m/%Y %H:%M:%S")
                        return cek, uang, pin, waktu
        time.sleep(2)
        return cek, uang, pin, waktu

    def deposit(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Deposit\n")
        cek = False
        uang = pin = waktu = 0
        try:
            uang = int(input(f"{'Uang tunai:': <16}{'': >10}"))
        except ValueError:            
            print("Masukan harus angka")
        else:
            if uang <= 0:
                print("Uang tidak boleh kurang dari 0")
            elif uang < 10000:
                print("Minimal tarik tunai 10.000")
            else:
                pin = input(f"{'Pin:': <20}{'': >10}")
                try:
                    int(pin)
                except ValueError:
                    print("Pin harus angka")
                else:
                    if int(pin) < 0:
                        print("Pin harus bilangan positif")
                    elif len(pin) != 4:
                        print("Pin berjumlah 4 digit")
                    else:
                        cek = True
                        waktu = time.strftime("%d/%m/%Y %H:%M:%S")
                        return cek, uang, pin, waktu                 
        time.sleep(2)
        return cek, uang, pin, waktu
    
    def transfer(self, msg):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Transfer\n\n{'saldo:': <25}{msg[3]: >10}")
        cek = False
        uang = pin = tujuan = waktu = 0
        try:
            tujuan = int(input(f"{'Rekening tujuan:': <18}{'': >10}"))
        except ValueError:            
            print("Masukan harus angka")
        else:
            if tujuan < 0:
                print("Rekening harus bilangan positif")
            elif len(str(tujuan)) != 5:
                print("Rekening berjumlah 5 digit")
            elif tujuan == int(msg[2]):
                print("Tidak dapat mengirim tujuan ke rekening sendiri")
            else:
                try:
                    uang = int(input(f"{'Jumlah uang tunai:': <16}{'': >10}"))
                except ValueError:            
                    print("Masukan harus angka")
                else:
                    if uang > int(msg[3]):
                        print("Saldo tidak mencukupi")
                    elif uang <= 0:
                        print("Uang tidak boleh kurang dari 0")
                    elif uang < 10000:
                        print("Minimal transfer 10.000")
                    else:
                        pin = input(f"{'Pin:': <18}{'': >10}")
                        try:
                            int(pin)
                        except ValueError:
                            print("Pin harus angka")
                        else:
                            if int(pin) < 0:
                                print("Pin harus bilangan positif")
                            elif len(pin) != 4:
                                print("Pin berjumlah 4 digit")
                            else:
                                cek = True
                                waktu = time.strftime("%d/%m/%Y %H:%M:%S")
                                return cek, tujuan, uang, pin, waktu
        time.sleep(2)
        return cek, tujuan, uang, pin, waktu

    def info(self, msg):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Nama\t\t: {msg[4]}\nNo rekening\t: {msg[2]}\nSaldo\t\t: {msg[3]}\n\nMutasi")
        mutasi = list(msg[5].split("&"))
        for i in mutasi:
            print(i)
        input("\nTekan ENTER untuk kembali")

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
                return f"register_2,{nama},{pin},{msg[2]},{msg[3]}"
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
                    cek, uang, pin, waktu = self.tarik_tunai(msg)
                    if cek:
                        return f"tarik_tunai,{msg[2]},{uang},{pin},{waktu}"
                    else:
                        return self.dashboard(msg)
                elif pilih == 2:
                    cek, uang, pin, waktu = self.deposit()
                    if cek:
                        return f"deposit,{msg[2]},{uang},{pin},{waktu}"
                    else:
                        return self.dashboard(msg)
                elif pilih == 3:
                    cek, tujuan, uang, pin, waktu = self.transfer(msg)
                    if cek:
                        return f"transfer,{msg[2]},{tujuan},{uang},{pin},{waktu}"
                    else:
                        return self.dashboard(msg)
                elif pilih == 4:
                    return f"info,{msg[2]}"
                elif pilih == 5:
                    return self.dashboard()
            else:
                print("Username atau password salah")
                time.sleep(2)
                return self.dashboard()
        elif msg[0] == "tarik_tunai" or msg[0] == "deposit" or msg[0] == "transfer":
            print(msg[4])
            time.sleep(2)
            msg[0] = "login"
            return self.dashboard(msg)
        elif msg[0] == "info":
            self.info(msg)
            msg[0] = "login"
            return self.dashboard(msg)

class Client(ATM):
    def __init__(self):
        self.mqttBroker ="mqtt.eclipseprojects.io"
        self.topicClient = "client"
        self.topicServer = f"server-{random.randrange(1, 999)}"

    def connect(self):
        self.client = mqtt.Client(f"Server-{random.randint(1, 999)}")
        self.client.connect(self.mqttBroker)

    def publish(self, teks):
        self.client.publish(self.topicClient, teks)
        print(f"publish {teks} dengan topic {self.topicClient}")

    def request(self, msg=["home"]):
        self.publish(f"{self.topicServer},{self.dashboard(msg)}")

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
    