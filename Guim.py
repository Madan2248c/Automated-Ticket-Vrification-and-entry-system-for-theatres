import tkinter as tk
from customtkinter import *
import cv2
from PIL import Image, ImageTk
import qr_detector


class QRApp:
    def __init__(self, root):
        self.root = root
        self.detector = None
        self.label_widget = None
        self.mainpage()

    def mainpage(self):
        self.root.geometry("1920x1080")
        self.root._set_appearance_mode("System")

        self.login_btn = CTkButton(master=self.root, text="Login")
        self.login_btn.place(x=1375, y=25)

        self.tabview = CTkTabview(master=self.root)
        self.tabview.pack(expand=True, fill="both", padx=0, pady=50)

        self.tabview.add('Entry')
        self.tabview.add('Exit')

        entry_frame = CTkFrame(master=self.tabview.tab('Entry'), border_width=2)
        entry_frame.pack(expand=True, fill="both")
        self.label_widget = CTkLabel(master=entry_frame, text="")
        self.label_widget.pack()

        start_cam_btn = CTkButton(master=entry_frame, text="Start cam", command=self.create_detector)
        start_cam_btn.pack()

        label1 = CTkLabel(master=self.tabview.tab('Entry'), text="This is Entry Side")
        label1.pack(padx=20, pady=20)

        label2 = CTkLabel(master=self.tabview.tab('Exit'), text="This is exit side")
        label2.pack(padx=20, pady=20)

    def create_detector(self):
        self.detector = qr_detector.QrDetector()
        self.open_camera()

    def open_camera(self):
        new_frame, output = self.detector.detect_from_a_frame()
        opencv_image = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGBA)

        captured_image = Image.fromarray(opencv_image)

        ctk_img = CTkImage(dark_image=captured_image, light_image=captured_image, size=(800, 600))

        self.label_widget.configure(image=ctk_img)
        
        if len(output) <= 0:
            self.label_widget.after(10, self.open_camera)
        else:
            self.label_widget.configure(image=None)
            self.label_widget.configure(text=output)
            print(output)

