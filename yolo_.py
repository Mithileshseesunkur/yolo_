import customtkinter






class root(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CTk example")

        #add video frame
        self.videoFrame=customtkinter.CTkFrame(self,border_width=1,width=720, height=480)

        self.videoFrame.grid(column=0,row=0, padx=20, pady=20)

        # add widgets to app
        self.button = customtkinter.CTkButton(self,text="Turn on", command=self.button_click)
        self.button.grid(row=1, column=0,padx=20,sticky="w")

    # add methods to app
    def button_click(self):
        print("button click")


app = root()
app.mainloop()