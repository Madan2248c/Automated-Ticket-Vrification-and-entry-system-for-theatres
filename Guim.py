from customtkinter import *
from tkinter import *
import cv2
from PIL import Image, ImageTk
import qr_detector

vid = cv2.VideoCapture(0)
width, height = 800, 600
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def open_camera():
    global vid
    if not vid.isOpened():
        vid = cv2.VideoCapture(0)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    ret, frame = vid.read()
    

    if not ret or frame is None:
        print("Error: Failed to capture frame")
        return
    
    detector = qr_detector.qr_detector()

    newframe = detector.detectfromaframe(frame)
    opencv_image = cv2.cvtColor(newframe, cv2.COLOR_BGR2RGBA)

    captured_image = Image.fromarray(opencv_image)

    ctkimg = CTkImage(dark_image=captured_image, light_image=captured_image, size=(800, 600))

    label_widget.configure(image=ctkimg)
    label_widget.after(10, open_camera)


app = CTk()
app.geometry("1920x1080")

tabview = CTkTabview(master=app)
tabview.pack(expand=True, fill="both")

tabview.add('Entry')
tabview.add('Exit')

entryFrame = CTkFrame(master=tabview.tab('Entry'), fg_color='#8D6F3A', border_width=2)
entryFrame.pack(expand=True, fill="both")
label_widget = CTkLabel(master=entryFrame, text="")
label_widget.pack()
startcambtn = CTkButton(master=entryFrame, text="Start cam", command=open_camera)
startcambtn.pack()

label1 = CTkLabel(master=entryFrame, text="This is Entry Side")
label1.pack(padx=20, pady=20)

label2 = CTkLabel(master=tabview.tab('Exit'), text="This is exit side")
label2.pack(padx=20, pady=20)

app.mainloop()
