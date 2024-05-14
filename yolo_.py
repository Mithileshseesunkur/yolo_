import customtkinter
from tkinter import *
import cv2
from PIL import Image, ImageTk

vid=cv2.VideoCapture(0)
width, height = 720,480
vid.set(cv2.CAP_PROP_FRAME_WIDTH,width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT,height)

webcam_running= False


class root(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        global webcam_running

        self.title("Webcam_yolo")

        #add video frame
        self.video_frame=customtkinter.CTkFrame(self,border_width=1,width=width, height=height)
        self.video_frame.grid(column=0,row=0, padx=20, pady=20, sticky="nsew")

        #add webcam buttons frame
        self.webcam_button_frame=customtkinter.CTkFrame(self,border_width=1,width=width, height=height)
        self.webcam_button_frame.grid(column=0, row=1, padx=20, pady=(0,20), sticky="w")

        #add video label
        self.video_label=customtkinter.CTkLabel(self.video_frame, width=width, height=height, text="")
        self.video_label.grid(row=0,column=0)

        # turn on button
        self.button = customtkinter.CTkButton(self.webcam_button_frame,text="Turn on", command=self.webcam_on)
        self.button.grid(row=1, column=0,padx=10, pady=(10),sticky="w")

        #turn off button
        self.button = customtkinter.CTkButton(self.webcam_button_frame, text="Turn off", command=self.webcam_off)
        self.button.grid(row=1, column=1,padx=(0,10), pady=(10), sticky="w")


    # turn on webcam
    def webcam_on(self):
        global webcam_running, vid
        
        if not webcam_running: #only turn on if webcam if off
            webcam_running= True
            print("Webcam on")

        


        #capture video fram by frame
        # try to get the first frame
    
        ret, frame=vid.read() # read a frame from the webcam
        print("webcam ruuning", webcam_running)

        

        #convert image from one colour space to another
        opencv_image= cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        #capture the latest frame and tansform to image
        captured_image= Image.fromarray(opencv_image)

        #convert captured image to photoimage
        self.photo_image= customtkinter.CTkImage(light_image=captured_image,size=(width,height))

        #displaying the photoimage in the label
        self.video_frame.photo_image=self.photo_image

        #configue image in the label            
        self.video_label.configure(image=self.photo_image)

        #repeat the same process every 10 seconds
        #self.video_label.after(10, self.webcam_on)

        # handle potential keyboard interrupt 
        if cv2.waitKey(10) == ord('q'):
            break


    # turn off webcam      qq
    def webcam_off(self):
        
        global webcam_running
        
        if webcam_running: # only turn off if webcam is on
            webcam_running= False

        #stop scheduled frame update
        self.video_label.after_cancel(self.webcam_on)

        # release the webcam recourses
        #if vid.isOpened():
            #vid.release()
        #webcam_running=False
        print("in webcam_off now",webcam_running)










app = root()
app.mainloop()