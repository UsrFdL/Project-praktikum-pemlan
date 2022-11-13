from tkinter import *
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Toko online")
        self.geometry("600x800")

        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.frame_1 = ctk.CTkFrame(master=self,
                                    height=112,
                                    corner_radius=0)
        self.frame_1.grid(row=0, column=0, sticky="nswe")
        self.label_1_f1 = ctk.CTkLabel(master=self.frame_1,
                                       text="Toko Online",
                                       text_font=("Inter", -64))
        self.label_1_f1.place(x=200, y=56, anchor="center")

        self.frame_2 = ctk.CTkFrame(master=self,
                                    height=58,
                                    corner_radius=0)
        # self.frame_2.grid(row=1, column=0, sticky="nswe")
        self.label_1_f2 = ctk.CTkLabel(master=self.frame_2,
                                       text="Kategori",
                                       text_font=("Noto Sans", -16))
        # self.label_1_f2.grid(row=0, column=0, sticky="e")


    def start(self):
        self.mainloop()

    def closing(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.start()