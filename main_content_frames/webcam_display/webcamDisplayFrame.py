import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

from .videoCapture import MyVideoCapture


class WebcamDisplayFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, allow_recording: bool, training_class=None, video_source: int = 0,
                 **kwargs):
        super().__init__(container, **kwargs)

        #       --properties--
        self.video_source = video_source
        # boolean for determining if recording from the webcam display is allowed
        self.allow_recording = allow_recording
        # boolean for determining if to record images from the webcam: controlled by the record button
        self.record = False
        # TrainingClass obj - the class that the recorded images will be saved to
        self.training_class = training_class
        # in update: contains the processed frame with ImageTk - to stop garbage collector from clearing the image
        self.photo = None

        # open video source (by default this will try to open the webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        # self.update()  # need to update before using winfo_width() / winfo_height()

        self.video_canvas = tk.Canvas(self, width=400, height=300)
        self.video_canvas.pack()

        # delay between each frame in milliseconds
        self.delay = 2

        # call update:
        self.update()

    #       --setters and getters--

    # sets self.record to the given status (T/F)
    def set_record(self, status: bool):
        self.record = status

    # ----------------------------------------------

    # update loop, updating the frames on the canvas
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        # print(cv2.resize(frame, dsize=(300, 300), interpolation=cv2.INTER_CUBIC).shape)
        if ret:  # check if we received a frame properly

            # record section:
            if self.allow_recording and self.record:  # record only when recording allowed and record = True
                # resize to the needed size
                width, height = (self.training_class.img_width, self.training_class.img_height)
                recorded_img = cv2.resize(frame, dsize=(width, height), interpolation=cv2.INTER_CUBIC)
                #  reshape to (1, width, height, 3)
                recorded_img = np.expand_dims(recorded_img, axis=0)
                # append to sample ndarray
                self.training_class.samples = np.append(self.training_class.samples, recorded_img, axis=0)
                # update sample counter label:
                self.training_class.class_frame.sample_counter += 1
                self.training_class.class_frame.sample_counter_label_text.set(f"{self.training_class.class_frame.sample_counter} image samples")

            # display webcam on canvas
            img = Image.fromarray(frame)
            img = img.resize((int(self.video_canvas["width"]), int(self.video_canvas["height"])), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(image=img)
            self.video_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.after(self.delay, self.update)
