import tkinter as tk
from customtkinter import *
import cv2
from PIL import Image, ImageTk
import databasemanager
import detectors
import time
import json


class QRApp:
    def __init__(self, root,user_logged_in):
        self.root = root
        self.user_logged_in = user_logged_in
        self.detector = None
        self.label_widget = None
        self.start_cam_btn = None
        self.no_of_allowedpersons = None
        self.manager = databasemanager.DatabaseManager(
        host='localhost',
        username='root',
        password='Madan@333',
        database='automated_entry_system'
        )
        self.mainpage()

    def mainpage(self):
        self.root.geometry("1920x1080")
        self.root._set_appearance_mode("System")

        self.login_btn = CTkButton(master=self.root, text=self.user_logged_in)
        self.login_btn.place(x=1375, y=25)

        self.tabview = CTkTabview(master=self.root)
        self.tabview.pack(expand=True, fill="both", padx=0, pady=50)

        self.tabview.add('Entry')
        self.tabview.add('Exit')

        entry_frame = CTkFrame(master=self.tabview.tab('Entry'), border_width=2)
        entry_frame.pack(expand=True, fill="both")
        self.label_widget = CTkLabel(master=entry_frame, text="")
        self.label_widget.pack()

        self.start_cam_btn = CTkButton(master=entry_frame, text="Start cam", command=self.create_detector)
        self.start_cam_btn.pack()

        self.no_of_allowedpersons = CTkLabel(master=entry_frame, text="g")
        self.no_of_allowedpersons.pack()

        label1 = CTkLabel(master=self.tabview.tab('Entry'), text="This is Entry Side")
        label1.pack(padx=20, pady=20)

        label2 = CTkLabel(master=self.tabview.tab('Exit'), text="This is exit side")
        label2.pack(padx=20, pady=20)

    def create_detector(self):
        self.start_cam_btn.destroy()
        self.detector = detectors.QrDetector()
        self.open_camera()

    def open_camera(self):
        new_frame, output = self.detector.detect_from_a_frame()
        opencv_image = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGBA)

        captured_image = Image.fromarray(opencv_image)

        ctk_img = CTkImage(dark_image=captured_image, light_image=captured_image, size=(600, 400))

        self.label_widget.configure(image=ctk_img)
        
        if len(output) <= 0:
            self.label_widget.after(10, self.open_camera)
        else:
            self.label_widget.configure(image=None)
            # self.label_widget.configure(text=output)
            ticket = json.loads(output)
            res = self.manager.check_ticket(ticket[0]['ticket_id'])
            if(res == 500):
                self.label_widget.configure(text="Already entered")
                return
            elif(res == 400):
                self.label_widget.configure(text="Ticket not found")
                return
            else:
                self.label_widget.configure(text="You can enter")
            print(ticket[0]['ticket_id'])
            self.no_of_allowedpersons.configure(text=output)
            self.start_pc()

    def start_pc(self):
        time.sleep(2)
        self.startpersoncounter()

    def startpersoncounter(self):
        new_frame, output = self.detector.detector()
        opencv_image = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGBA)

        captured_image = Image.fromarray(opencv_image)

        ctk_img = CTkImage(dark_image=captured_image, light_image=captured_image, size=(600, 400))

        self.label_widget.configure(image=ctk_img)
        
        if (output) <= 3:
            self.label_widget.after(10, self.startpersoncounter)
        else:
            self.label_widget.configure(image=None)
            self.label_widget.configure(text=output)
            print(output)