import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from .webcamDisplayFrame import WebcamDisplayFrame
# from main_content_frames.test_section_frames.testImageDisplaySectionFrame import TestImageDisplaySectionFrame


# inherits WebcamDisplayFrame - overriding the update method (configuring it for the prediction part)
class TestWebcamDisplayFrame(WebcamDisplayFrame):
    def __init__(self, container: ttk.Frame, test_image_display_section, video_source: int = 0,
                 **kwargs):
        super().__init__(container, video_source=video_source, **kwargs)

        self.test_image_display_section = test_image_display_section

        # call self.update
        self.update()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        # check if we received a frame properly
        if ret:

            # predict on the frame:

            # resize img
            img = cv2.resize(frame, dsize=(128, 128), interpolation=cv2.INTER_CUBIC)
            # pre-process input & and add batch_size dimension
            img = preprocess_input(img)[np.newaxis, ...]
            # predict:
            self.test_image_display_section.display_predictions_on_img(img, self.test_image_display_section.preds_window.prediction_frames)

            # display webcam on canvas
            display_img = Image.fromarray(frame)
            display_img = display_img.resize((int(self.video_canvas["width"]), int(self.video_canvas["height"])), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(image=display_img)
            self.video_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.after(self.delay, self.update)
