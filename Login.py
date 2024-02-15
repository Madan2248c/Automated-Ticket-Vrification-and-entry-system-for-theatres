import tkinter as tk
from tkinter import messagebox
from customtkinter import *
from Guim import QRApp
import databasemanager
class LoginPage:
    def __init__(self, master):
        self.master = master

        master.geometry("1920x1080")
        master._set_appearance_mode("System")
        master.title("Login Page")

        bg_image_path = "pxfuel.png"
        self.bg_image = tk.PhotoImage(file=bg_image_path)

        self.canvas = CTkCanvas(master=master, width=1920, height=1080)
        self.canvas.pack(fill='both', expand=True)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

        self.frame = CTkFrame(master=self.canvas, bg_color="#161618", fg_color="#161618")
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        self.manager = databasemanager.DatabaseManager(
        host='localhost',
        username='root',
        password='Madan@333',
        database='automated_entry_system'
        )

        self.create_widgets()

    def create_widgets(self):
        header_label = CTkLabel(master=self.frame, text="LOGIN", font=("Arial", 40, "bold"))
        header_label.pack(side=tk.TOP, pady=(0, 20))

        entry_width = 200
        self.user_entry = CTkEntry(master=self.frame, placeholder_text="Username", width=entry_width)
        self.user_entry.pack(side=tk.TOP, pady=(0, 30))

        self.user_pass = CTkEntry(master=self.frame, placeholder_text="Password", show="*", width=entry_width)
        self.user_pass.pack(side=tk.TOP, pady=(0, 30))

        button_width = 200
        button = CTkButton(master=self.frame, text='Login', width=button_width, command=self.handle_login)
        button.pack(side=tk.TOP)

        forgot_label = CTkLabel(master=self.frame, text="Forgot Password?", cursor="hand2")
        forgot_label.pack(side=tk.RIGHT, pady=(0, 30), padx=(0, 40))

        self.frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.frame.place(relx=0.5, rely=0.533, anchor=tk.CENTER)

    def handle_login(self):
        username = self.user_entry.get()
        password = self.user_pass.get()

        result = self.manager.check_user(username,password)

        if result:
            messagebox.showinfo("Login Successful", "Welcome, " + result[0][1] + "!")
            self.master.destroy()
            root1 = CTk()
            app = QRApp(root1,result[0][1])
            root1.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")