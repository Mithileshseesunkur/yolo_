import customtkinter
from tkinter import *
import cv2
from PIL import Image, ImageTk



#webcam_running= None


class root(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.initialise_webcam()

        self.webcam_running=True

        self.title("Webcam_yolo")

        #add video frame
        self.video_frame=customtkinter.CTkFrame(self,border_width=1,width=self.width, height=self.height)
        self.video_frame.grid(column=0,row=0, padx=20, pady=20, sticky="nsew")

        #add webcam buttons frame
        self.webcam_button_frame=customtkinter.CTkFrame(self,border_width=1,width=self.width, height=self.height)
        self.webcam_button_frame.grid(column=0, row=1, padx=20, pady=(0,20), sticky="w")

        #add video label
        self.video_label=customtkinter.CTkLabel(self.video_frame, width=self.width, height=self.height, text="")
        self.video_label.grid(row=0,column=0)

        # turn on button
        self.button = customtkinter.CTkButton(self.webcam_button_frame,text="Turn on", command=self.webcam_on)
        self.button.grid(row=1, column=0,padx=10, pady=(10),sticky="w")

        #turn off button
        self.button = customtkinter.CTkButton(self.webcam_button_frame, text="Turn off", command=self.webcam_off)
        self.button.grid(row=1, column=1,padx=(0,10), pady=(10), sticky="w")



    def initialise_webcam(self):
        self.vid=cv2.VideoCapture(0)
        self.width, self.height = 720,480
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH,self.width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT,self.height)

    # turn on webcam
    def webcam_on(self):
        
        #capture video fram by frame
        # try to get the first frame
        #self.initialise_webcam()
        self.ret, self.frame=self.vid.read() # read a frame from the webcam
        print("webcam running", self.webcam_running)

        if not self.ret:
            self.initialise_webcam()
            print("webcam again")
            self.webcam_running=True
            self.ret, self.frame=self.vid.read()
            

        
        #self.webcam_running=True

        #convert image from one colour space to another
        self.opencv_image= cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)

        #capture the latest frame and tansform to image
        self.captured_image= Image.fromarray(self.opencv_image)

        #convert captured image to photoimage
        self.photo_image= customtkinter.CTkImage(light_image= self.captured_image,size=(self.width,self.height))

        #displaying the photoimage in the label
        self.video_frame.photo_image=self.photo_image

        #configue image in the label            
        self.video_label.configure(image=self.photo_image)

        #repeat the same process every 10 seconds
        if self.webcam_running:
            self.video_label.after(10, self.webcam_on)

        else:
            #self.video_label.after_cancel(self.webcam_on)
            #self.webcam_running=False
            print("in else loop")
            #self.after_id=None
            self.vid.release()
        # handle potential keyboard interrupt 
        # if cv2.waitKey(10) == ord('q'):

                


    # turn off webcam      qq
    def webcam_off(self):
        
        
        if self.webcam_running: # only turn off if webcam is on
            self.webcam_running= False

        #stop scheduled frame update
        #self.video_label.after_cancel(self.webcam_on)

        # release the webcam recourses
        #if vid.isOpened():
            #vid.release()
        #webcam_running=False
        print("in webcam_off now",self.webcam_running)










app = root()
app.mainloop()