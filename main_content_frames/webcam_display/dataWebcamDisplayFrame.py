import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

from .webcamDisplayFrame import WebcamDisplayFrame


# inherits WebcamDisplayFrame - overriding the update method (configuring it for the recording part)
class DataWebcamDisplayFrame(WebcamDisplayFrame):
    def __init__(self, container: ttk.Frame, training_class=None, video_source: int = 0,
                 **kwargs):
        super().__init__(container, video_source, **kwargs)

        # boolean for determining if to record images from the webcam: controlled by the record button
        self.record = False
        # TrainingClass obj - the class that the recorded images will be saved to
        self.training_class = training_class

        # call update:
        self.update()

    # sets self.record to the given status (T/F)
    def set_record(self, status: bool):
        self.record = status

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        # check if we received a frame properly
        if ret:

            # record section:
            if self.record:  # record only when record = True
                # resize to the needed size
                width, height = (self.training_class.img_width, self.training_class.img_height)
                recorded_img = cv2.resize(frame, dsize=(width, height), interpolation=cv2.INTER_CUBIC)
                #  reshape to (1, width, height, 3)
                recorded_img = np.expand_dims(recorded_img, axis=0)
                # append to sample ndarray
                self.training_class.samples = np.append(self.training_class.samples, recorded_img, axis=0)
                # update sample counter label:
                self.training_class.sample_counter += 1
                self.training_class.class_frame.sample_counter_label_text.set(
                    f"{self.training_class.sample_counter} image samples")

            # display webcam on canvas
            img = Image.fromarray(frame)
            img = img.resize((int(self.video_canvas["width"]), int(self.video_canvas["height"])), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(image=img)
            self.video_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.after(self.delay, self.update)
