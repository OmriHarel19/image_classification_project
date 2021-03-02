import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from .videoCapture import MyVideoCapture


class WebcamDisplayFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, video_source: int = 0, **kwargs):
        super().__init__(container, **kwargs)

        #       --properties--
        self.video_source = video_source
        self.photo = None

        # open video source (by default this will try to open the webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        # self.update()  # need to update before using winfo_width() / winfo_height()

        self.video_canvas = tk.Canvas(self, width=400, height=300)
        self.video_canvas.pack()

        # delay between each frame in milliseconds
        self.delay = 5

        # call update:
        self.update()

    # update loop, updating the frames on the canvas
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            img = Image.fromarray(frame)
            img = img.resize((int(self.video_canvas["width"]), int(self.video_canvas["height"])), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(image=img)
            self.video_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.after(self.delay, self.update)
