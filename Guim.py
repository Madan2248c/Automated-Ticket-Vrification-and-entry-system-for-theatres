from tkinter import messagebox 
from customtkinter import *
import cv2
from PIL import Image
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
        self.exit_cam_btn = None
        self.exit_label = None
        self.no_of_allowedpersons = None
        self.no_of_allowedpersons1 = None
        self.manager = databasemanager.DatabaseManager(
        host='localhost',
        username='root',
        password='Madan@333',
        database='automated_entry_system'
        )
        self.exit_frame = None
        self.start_time = None
        self.no_of_left = None
        self.exit_ticket = None
        self.max_per = 0
        self.mainpage()

    def mainpage(self):
        self.root.geometry("1920x1080")
        self.root._set_appearance_mode("System")

        self.login_btn = CTkButton(master=self.root,text=self.user_logged_in,command=self.logout)
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

        self.no_of_allowedpersons = CTkLabel(master=entry_frame, text="")
        self.no_of_allowedpersons.pack()

        label1 = CTkLabel(master=self.tabview.tab('Entry'), text="This is Entry Side")
        label1.pack(padx=20, pady=20)

        self.exit_frame = CTkFrame(master=self.tabview.tab('Exit'), border_width=2)
        self.exit_frame.pack(expand=True, fill="both")

        self.exit_cam_btn = CTkButton(master=self.exit_frame, text="Start cam", command=self.exit_detector)
        self.exit_cam_btn.pack()

        self.no_of_left = CTkLabel(master=self.exit_frame, text="")
        self.no_of_left.pack()

        self.exit_label = CTkLabel(master=self.exit_frame, text="")
        self.exit_label.pack()
               

        label2 = CTkLabel(master=self.tabview.tab('Exit'), text="This is exit side")
        label2.pack(padx=20, pady=20)


    def exit_detector(self):
        self.exit_cam_btn.destroy()
        self.exit_label.destroy()
        self.exit_label = CTkLabel(master=self.exit_frame, text="")
        self.exit_label.pack()
        if self.detector is not None:
            del self.detector
            self.detector = detectors.QrDetector()
            self.exit_check()
        else:
            self.detector = detectors.QrDetector()
            self.exit_check()

    def exit_check(self):
        new_frame,output = self.detector.detect_from_a_frame()
        opencv_image = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGBA)
        image = Image.fromarray(opencv_image)
        ctk_img = CTkImage(dark_image=image, light_image=image, size=(600, 400))
        self.exit_label.configure(image=ctk_img)
        if len(output) <= 0:
            self.exit_label.after(10, self.exit_check)
        else:
            self.exit_label.configure(image=None)
            self.exit_label.configure(text=output)
            self.exit_ticket = json.loads(output)
            self.ini_exit_pc()

    def ini_exit_pc(self):
        self.start_time = time.time()
        self.maxpersons()

    def maxpersons(self):
        out = self.manager.check_if_exit(self.exit_ticket[0]['ticket_id'])
        if out is not None:
            self.max_per = self.exit_ticket[0]['persons_allowed'] - out[1]
        else:
            self.max_per = self.exit_ticket[0]['persons_allowed']
        messagebox.showinfo("Max persons","maximum only "+str(self.max_per) + "can go out")
        self.exit_pc()

    def exit_pc(self):
        self.exit_label.configure(text=None)
        new_frame,output,cmp = self.detector.count_persons_in10sec(self.start_time)
        if cmp == 1 or output >= self.max_per:

            if output >= self.max_per:
                messagebox.showinfo("Persons","Maximum number of persons have been exited")
            self.exit_label.configure(image=None)
            self.no_of_left.configure(text=output)
            self.exit_cam_btn = CTkButton(master=self.exit_frame, text="Start cam", command=self.exit_detector)
            self.exit_cam_btn.pack()
            self.manager.add_to_exit(self.exit_ticket[0]['ticket_id'],output)
        else :
            opencv_image = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGBA)
            image = Image.fromarray(opencv_image)
            ctk_img = CTkImage(dark_image=image, light_image=image, size=(600, 400))
            self.exit_label.configure(image=ctk_img)

            self.exit_label.after(10, self.exit_pc)
            
    def create_detector(self):
        self.start_cam_btn.destroy()
        self.label_widget.configure(text="")
        if self.detector is not None:
            del self.detector
            self.detector = detectors.QrDetector()
            self.open_camera()
        else:
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
            ticket = json.loads(output)
            res,nop = self.manager.check_ticket(ticket[0]['ticket_id'])
            if(res == 200):
                self.no_of_allowedpersons1 = nop
            elif(res == 500):
                messagebox.showinfo("Ticketet status","Already entered")
                self.create_detector()
                return
            elif(res == 400):
                messagebox.showinfo("Ticketet status","Already entered")
                self.create_detector()
                return
            else:
                # self.label_widget.configure(text="You can enter")
                print(ticket[0]['persons_allowed'])
                self.no_of_allowedpersons1 = ticket[0]['persons_allowed']
                no_per = "Number of persons to enter is " + str(ticket[0]['persons_allowed'])
                self.no_of_allowedpersons.configure(text=no_per)
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
        
        if (output) < self.no_of_allowedpersons1:
            self.label_widget.after(10, self.startpersoncounter)
        else:
            self.label_widget.configure(image=None)
            self.label_widget.configure(text=output)
            self.create_detector()
            print(output)

    def logout(self):
        res = messagebox.askquestion("Logout" , "Are you sure that you want to close the system")
        if res == 'yes':
            self.root.destroy()
        else:
            return
        
if __name__ == "__main__":
    root = CTk()
    app = QRApp(root,"madan")
    root.mainloop()