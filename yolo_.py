import customtkinter
from tkinter import *
import cv2
from PIL import Image, ImageTk

cap=cv2.VideoCapture(0)
width, height = 720,480
cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)





class root(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CTk example")

        #add video frame
        self.videoFrame=customtkinter.CTkFrame(self,border_width=1,width=720, height=480)
        self.videoFrame.grid(column=0,row=0, padx=20, pady=20, sticky="nsew")

        # add widgets to app
        self.button = customtkinter.CTkButton(self,text="Turn on", command=self.webcamOn)
        self.button.grid(row=1, column=0,padx=20, pady=(0,20),sticky="w")

    # add methods to app
    def webcamOn(self):
        print("button click")


app = root()
app.mainloop()