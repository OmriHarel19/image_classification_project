import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from PIL import Image, ImageTk
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from main_content_frames.webcam_display import *
from main_content_frames.train_section.mobileNetModel import MnetModel
from .predictionsWindow import PredictionsWindow
from .predictionFrame import PredictionFrame

from typing import List


class TestImageDisplaySectionFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, predictions_window: PredictionsWindow, **kwargs):
        super().__init__(container, **kwargs)

        self.upload_img = None
        self.trained_classifier = None

        self.preds_window = predictions_window

        # row & col config:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # row 0: webcam & upload buttons
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.grid(row=0, column=0, padx=5, pady=5, sticky="EW")

        # webcam buttons containter
        self.webcam_buttons_container = ttk.Frame(self.buttons_frame)
        self.webcam_buttons_container.columnconfigure(0, weight=1)
        self.webcam_buttons_container.grid(row=0, column=0, padx=5, pady=5, sticky="EW")

        # webcam button:
        self.webcam_button = ttk.Button(
            self.webcam_buttons_container,
            text="webcam",
            state="disabled",  # test section starts disabled
            command=self.webcam_display
        )
        self.webcam_button.grid(row=0, column=0, padx=2, pady=2, sticky="W")

        # stop webcam button:
        self.stop_webcam_button = ttk.Button(
            self.webcam_buttons_container,
            text="stop webcam",
            state="disabled",  # test section starts disabled
            command=self.stop_webcam
        )
        self.stop_webcam_button.grid(row=1, column=0, padx=2, pady=2, sticky="W")

        # upload button:
        self.upload_button = ttk.Button(
            self.buttons_frame,
            text="upload",
            state="disabled",  # test section starts disabled
            command=self.upload_test_image
        )
        self.upload_button.grid(row=0, column=1, padx=2, pady=2, sticky="W")

        self.buttons_list = [self.webcam_button, self.stop_webcam_button, self.upload_button]

        # row 1: image display frame: for image upload & webcam display
        # contains both display label for upload and display canvas for webcam
        # switching frame with tkraise()

        self.image_display_frame = ttk.Frame(self, style="Background1.TFrame")
        self.image_display_frame.columnconfigure(0, weight=1)
        self.image_display_frame.rowconfigure(0, weight=1)
        self.image_display_frame.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")

        # webcam display canvas

        self.webcam_display_container = ttk.Frame(self.image_display_frame)
        # self.webcam_display_container.columnconfigure(0, weight=1)
        # self.webcam_display_container.rowconfigure(0, weight=1)
        self.webcam_display_container.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

        # upload display label
        self.display_label_container = ttk.Frame(self.image_display_frame)
        # self.display_label_container.columnconfigure(0, weight=1)
        # self.display_label_container.rowconfigure(0, weight=1)
        self.display_label_container.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

        self.display_label = ttk.Label(
            self.display_label_container,
            anchor="center",
            text="image testing display",
            font=("TkDefaultFont", 15),
        )
        self.display_label.pack(expand=True, fill="both", padx=5, pady=5)
        ''''''

    # setters & getters:

    def set_trained_classifier(self, trained_classifier: MnetModel):
        self.trained_classifier = trained_classifier

    # ------------------------------------------------------------------------------------------

    # triggered by the upload button - upload test image from file explorer and display in image_display_frame
    def upload_test_image(self):
        # destroy all existing objects inside webcam_display_container
        for child in self.webcam_display_container.winfo_children():
            child.destroy()

        # open file explorer:
        file_path = tk.filedialog.askopenfilename(  # returns a tuple of selected file paths
            initialdir=os.getcwd(),
            title="Select Image file",
            filetypes=(("JPG File", "*.jpg"), ("JPEG File", "*.jpeg"), ("PNG File", "*.png"))
        )

        if file_path != "":  # check that a file was selected
            # ----load image for display----
            self.upload_img = Image.open(file_path)
            self.upload_img.thumbnail((300, 300))
            self.upload_img = ImageTk.PhotoImage(self.upload_img)
            # put on label
            self.display_label.configure(image=self.upload_img)
            self.display_label.image = self.upload_img

            # raise frame
            self.display_label_container.tkraise()

            # ----load image for model----
            img = load_img(file_path, color_mode='rgb', target_size=(128, 128))  # remember to change the hard code
            img = img_to_array(img)[np.newaxis, ...]  # add the batch_size dimension
            img = preprocess_input(img)  # pre-process input
            # predict:
            self.display_predictions_on_img(img, self.preds_window.prediction_frames)

    # triggered by the webcam button - display webcam footage in image_display_frame
    def webcam_display(self):
        # destroy all existing objects inside webcam_section_frame.webcam_display_container (from any other class)

        try:
            # create WebcamDisplayFrame inside image_display_frame
            webcam_display = WebcamDisplayFrame(self.webcam_display_container, allow_recording=False,
                                                training_class=None, video_source=0)
            webcam_display.grid(row=0, column=0, sticky="NSEW")

            # raise frame
            self.webcam_display_container.tkraise()

        except ValueError:
            self.display_label["text"] = "no video source detected"

    # triggered by the stop webcam button -stop the webcam display
    def stop_webcam(self):
        # destroy all existing objects inside webcam_section_frame.webcam_display_container (from any other class)
        for child in self.webcam_display_container.winfo_children():
            child.destroy()

    def display_predictions_on_img(self, img_array: np.array, prediction_frames_list: List[PredictionFrame]):
        # use model to predict on the given img
        prediction = self.trained_classifier.model.predict(img_array)
        print(f"prediction: {prediction}")

        # in case its a binary classifier: (a single prediction value is returned)
        if self.trained_classifier.get_number_of_classes() == 2:
            prediction_frames_list[0].set_prediction(1.0 - float(np.squeeze(prediction)))
            print(f"pred of {prediction_frames_list[0].get_class_name()}: {1.0 - float(np.squeeze(prediction))}")
            prediction_frames_list[1].set_prediction(float(np.squeeze(prediction)))
            print(f"pred of {prediction_frames_list[1].get_class_name()}: {float(np.squeeze(prediction))}")
        else:
            for i, pred_frame in enumerate(prediction_frames_list):
                pred_frame.set_prediction(float(np.squeeze(prediction[i])))
