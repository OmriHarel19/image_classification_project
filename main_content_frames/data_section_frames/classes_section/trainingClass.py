import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import os
from PIL import Image, ImageTk

import numpy as np
# import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

from main_content_frames.data_section_frames.classes_section.classFrame import ClassFrame

from main_content_frames.data_section_frames.webcam_section.dataWebcamSectionFrame import DataWebcamSectionFrame

from main_content_frames.webcam_display import *

#       --constants--

IMG_HEIGHT = 224
IMG_WIDTH = 224


# -----------------------------------------

# a training class object, contains the:
# classFrame, class samples and class state
class TrainingClass:
    def __init__(self, container: ttk.Frame, class_num: int, webcam_section_frame: DataWebcamSectionFrame, **kwargs):

        #       --properties--
        self.img_width, self.img_height = (224, 224)
        self.samples = np.empty(shape=(0, self.img_width, self.img_height, 3))  # 4 dim array containing class image samples
        self.enabled = True  # boolean state of the class
        self.class_frame = ClassFrame(container=container, class_num=class_num)

        # set button commands
        self.class_frame.upload_button["command"] = self.upload_images
        self.class_frame.webcam_button["command"] = lambda: self.display_webcam(webcam_section_frame)
        # set option list binding
        self.class_frame.options_combobox.bind("<<ComboboxSelected>>", self.options_menu)
        self.class_frame.options_combobox.set("enable class")

    #       --setters & getters--

    def get_class_name(self):
        return self.class_frame.class_name_textbox.get("1.0", "end")

    # ----------------------------------------------

    # triggered when the upload button of a specific class is pressed
    # opens file explorers and saves the selected images into self.samples using keras.preprocessing
    def upload_images(self):
        # open file explorer:

        file_paths = tk.filedialog.askopenfilenames(  # returns a tuple of selected file paths
            initialdir=os.getcwd(),
            title="Select Image file",
            filetypes=(("JPG File", "*.jpg"), ("JPEG File", "*.jpeg"), ("PNG File", "*.png"))
        )

        # load images into self.samples
        if type(file_paths) == tuple:  # when file/s are selected askopenfilenames returns a tuple of paths

            # create empty np array for selected images
            current_samples = np.empty((len(file_paths), self.img_width, self.img_height, 3))

            for idx, img_path in enumerate(file_paths):
                # load img
                img = load_img(img_path, color_mode='rgb', target_size=(self.img_width, self.img_height))
                print("Original:", type(img))

                # convert to numpy array
                img_array = img_to_array(img)
                print(f"img_array shape {img_array.shape}")

                # add to samples:
                current_samples[idx] = img_array  # np.append returns a copy of the array

            # add new samples to data set with np.concatenate
            self.samples = np.concatenate((self.samples, current_samples), axis=0)

            # array after addition:
            print(f"self.samples shape: {self.samples.shape}")

            # update sample counter label:
            self.class_frame.sample_counter += current_samples.shape[0]
            self.class_frame.label_text.set(f"{self.class_frame.sample_counter} image samples")

    # triggered when the webcam button of a specific class is pressed
    # creates a new WebcamDisplayFrame for the current class, and displays webcam footage
    def display_webcam(self, webcam_section_frame: DataWebcamSectionFrame):

        # destroy all existing objects inside webcam_section_frame.webcam_display_container (from any other class)
        webcam_section_frame.stop_webcam()

        try:
            # create WebcamDisplayFrame inside DataWebcamSectionFrame
            webcam_display = WebcamDisplayFrame(webcam_section_frame.webcam_display_container, allow_recording=True,
                                                training_class=self, video_source=0)
            webcam_display.grid(row=0, column=0, sticky="NSEW")

            # add the calling class name
            curr_class_name = self.class_frame.class_name_textbox.get("1.0", "end")
            webcam_section_frame.current_class_name.set(curr_class_name)

        except ValueError:
            webcam_section_frame.current_class_label["text"] = "no video source detected"

        # disable webcam button:
        # self.class_frame.webcam_button["state"] = "disabled"

    # triggered when an option is selected from the option combobox of a certain class
    # calls the method of the selected option
    def options_menu(self, event):  # event = ComboboxSelected - a selection of one of the options

        # options dict: keys=option, values=function to call
        options = {"delete class": self.delete,
                   "disable class": self.disable_class,
                   "enable class": self.enable_class,
                   "delete all samples": self.delete_samples
                   }

        # call the selected option method
        options[self.class_frame.current_option.get()]()

    #       --options methods--
    def delete(self):
        self.class_frame.destroy()
        del self

    def disable_class(self):
        self.enabled = False
        print(f"class {self.class_frame.class_name} is disabled")

    def enable_class(self):
        self.enabled = True
        print(f"class {self.class_frame.class_name} is enabled")

    def delete_samples(self):
        # initialize sample as an empty np array
        self.samples = np.empty(shape=(0, self.img_width, self.img_height, 3))
        # update sample counter
        self.class_frame.sample_counter = 0
        self.class_frame.label_text.set(f"{self.class_frame.sample_counter} image samples")
