import customtkinter
from tkinter import *
import cv2
from PIL import Image, ImageTk
import time
import threading
from ultralytics import YOLO

start_time = time.time()

class root(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.initialise = True  # param to initialise camera one time only
        self.width, self.height = 720, 480  # Define the width and height

        # initialise webcam only one time
        if self.initialise:
            self.initialise_webcam()

        self.initialise = False

        self.webcam_running = False
        self.thread = None
        self.lock = threading.Lock()

        self.title("Webcam_yolo")

        customtkinter.set_appearance_mode("dark")

        

        # add video frame
        self.video_frame = customtkinter.CTkFrame(self, border_width=1, width=self.width, height=self.height)
        self.video_frame.grid(column=0, row=0, padx=20, pady=20, sticky="nsew")

        # add webcam buttons frame
        self.webcam_button_frame = customtkinter.CTkFrame(self, border_width=1, width=self.width, height=self.height)
        self.webcam_button_frame.grid(column=0, row=1, padx=20, pady=(0, 20), sticky="w")

        # add video label
        self.video_label = customtkinter.CTkLabel(self.video_frame, width=self.width, height=self.height, text="")
        self.video_label.grid(row=0, column=0)

        # turn on button
        self.button_on = customtkinter.CTkButton(self.webcam_button_frame, text="Turn on", command=self.webcam_on)
        self.button_on.grid(row=1, column=0, padx=10, pady=(10), sticky="w")

        # turn off button
        self.button_off = customtkinter.CTkButton(self.webcam_button_frame, text="Turn off", command=self.webcam_off)
        self.button_off.grid(row=1, column=1, padx=(0, 10), pady=(10), sticky="w")
        self.button_off.configure(state="disabled")

    def initialise_webcam(self):
        self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # remove 2nd arg if not running on a laptop
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
    
        # initialise yolo model
        self.model = YOLO('yolov8m.pt')

    def yolo_detection(self):
        while self.webcam_running:
            with self.lock:
                frame = self.frame.copy()
            self.result = self.model(frame)
            time.sleep(0.1)  # Adjust as necessary for performance

    def webcam_capture(self):
        while self.webcam_running:
            self.ret, self.frame = self.vid.read()  # read a frame from the webcam
            if not self.ret:
                continue

            # convert image from one color space to another
            self.opencv_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)

            # capture the latest frame and transform to image
            self.captured_image = Image.fromarray(self.opencv_image)

            # convert captured image to photoimage
            self.photo_image = customtkinter.CTkImage(light_image=self.captured_image, size=(self.width, self.height))

            # displaying the photoimage in the label
            self.video_frame.photo_image = self.photo_image

            # configure image in the label
            self.video_label.configure(image=self.photo_image)

            time.sleep(0.01)  # Adjust as necessary for performance

    def webcam_on(self):
        if not self.webcam_running:
            self.webcam_running = True
            self.button_on.configure(state="disabled")
            self.button_off.configure(state="normal")
            self.capture_thread = threading.Thread(target=self.webcam_capture)
            self.capture_thread.start()
            self.detection_thread = threading.Thread(target=self.yolo_detection)
            self.detection_thread.start()

    def webcam_off(self):
        if self.webcam_running:
            self.webcam_running = False
            self.capture_thread.join()
            self.detection_thread.join()
            self.vid.release()
            self.button_on.configure(state="normal")
            self.button_off.configure(state="disabled")

app = root()
app.mainloop()

end_time = time.time()
print(end_time - start_time)
