import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        # checks if video source opened:
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # get a frame from the webcam
    def get_frame(self):
        ret = False
        # if camera active:
        if self.vid.isOpened():
            ret, frame = self.vid.read()  # read: returns a frame and a bool, indicating if the frame was read correctly
            frame = cv2.flip(frame, 1)  # flip img on the vertical axis

            if ret:
                # Return a boolean success flag and the current frame converted to RGB
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return ret, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
