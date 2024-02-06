import tkinter as tk
from tkinter import messagebox
import threading
import time

def countdown():
    for i in range(5, -1, -1):
        countdown_label.config(text=f"Countdown: {i}")
        time.sleep(1)
    messagebox.showinfo("Countdown", "Time's up!")

def start_countdown():
    threading.Thread(target=countdown).start()

root = tk.Tk()
root.title("Countdown")

countdown_label = tk.Label(root, text="Countdown: ")
countdown_label.pack(pady=10)

start_button = tk.Button(root, text="Start", command=start_countdown)
start_button.pack(pady=10)

root.mainloop()
