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

from main_content_frames.webcam_display.dataWebcamDisplayFrame import DataWebcamDisplayFrame

from typing import List

#       --constants--

IMG_HEIGHT = 224
IMG_WIDTH = 224


# -----------------------------------------

# a training class object, contains the:
# classFrame, class samples and class state
class TrainingClass:
    def __init__(self, container: ttk.Frame, class_num: int, classes_list: List,
                 webcam_section_frame: DataWebcamSectionFrame, **kwargs):

        #       --properties--
        self.img_width, self.img_height = (128, 128)
        self.minimal_dataset_size = 128
        self.sample_counter = 0
        self.samples = np.empty(
            shape=(0, self.img_width, self.img_height, 3))  # 4 dim array containing class image samples
        self.enabled = True  # boolean state of the class
        self.class_frame = ClassFrame(container=container, class_num=class_num)

        # set button commands
        self.class_frame.upload_button["command"] = self.upload_images
        self.class_frame.webcam_button["command"] = lambda: self.display_webcam(webcam_section_frame)
        # set option list binding
        self.class_frame.options_combobox.bind("<<ComboboxSelected>>",
                                               lambda event: self.options_menu(event, classes_list=classes_list))
        self.class_frame.options_combobox.set("enable class")

    #       --setters & getters--

    def get_class_name(self):
        return self.class_frame.class_name.get()

    def get_minimal_dataset_size(self):
        return self.minimal_dataset_size

    def is_enabled(self):
        return self.enabled

    def is_dataset_empty(self):
        return self.samples.shape[0] == 0

    def is_minimal_dataset_size(self):
        return self.sample_counter >= self.minimal_dataset_size

    # ----------------------------------------------

    # triggered when the upload button of a specific class is pressed
    # opens file explorers and saves the selected images into self.samples using keras.preprocessing
    def upload_images(self):
        # open file explorer:

        file_paths = filedialog.askopenfilenames(  # returns a tuple of selected file paths
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

            # update sample counter & sample counter label label:
            self.sample_counter += current_samples.shape[0]
            self.class_frame.sample_counter_label_text.set(f"{self.sample_counter} image samples")

    # triggered when the webcam button of a specific class is pressed
    # creates a new WebcamDisplayFrame for the current class, and displays webcam footage
    def display_webcam(self, webcam_section_frame: DataWebcamSectionFrame):

        # destroy all existing objects inside webcam_section_frame.webcam_display_container (from any other class)
        webcam_section_frame.stop_webcam()

        try:
            # create WebcamDisplayFrame inside DataWebcamSectionFrame
            webcam_display = DataWebcamDisplayFrame(webcam_section_frame.webcam_display_container,
                                                    training_class=self, video_source=0)
            webcam_display.grid(row=0, column=0, sticky="NSEW")

            # add the calling class name
            curr_class_name = self.get_class_name()
            webcam_section_frame.current_class_name.set(curr_class_name)

        except ValueError:
            webcam_section_frame.current_class_label["text"] = "no video source detected"

        # disable webcam button:
        # self.class_frame.webcam_button["state"] = "disabled"

    # triggered when an option is selected from the option combobox of a certain class
    # calls the method of the selected option
    def options_menu(self, event, classes_list):  # event = ComboboxSelected - a selection of one of the options

        # delete is a special option - requires the classes list to remove the Training class obj from the
        if self.class_frame.current_option.get() == "delete class":
            self.delete(classes_list)
        else:
            # options dict: keys=option, values=function to call
            options = {"disable class": self.disable_class,
                       "enable class": self.enable_class,
                       "delete all samples": self.delete_samples
                       }

            # call the selected option method
            options[self.class_frame.current_option.get()]()

    #       --options methods--

    def delete(self, classes_list: List):
        # remove the TrainingClass obj from the classes list
        for training_class in classes_list:
            if training_class == self:  # comparing pointers
                classes_list.remove(training_class)
        # destroy the ttk class frame
        self.class_frame.destroy()
        # delete self
        del self

    def disable_class(self):
        self.enabled = False
        self.class_frame.class_state_label_text.set(f"class disabled")

    def enable_class(self):
        self.enabled = True
        self.class_frame.class_state_label_text.set(f"class enabled")

    def delete_samples(self):
        # initialize sample as an empty np array
        self.samples = np.empty(shape=(0, self.img_width, self.img_height, 3))
        # update sample counter
        self.class_frame.sample_counter = 0
        self.class_frame.sample_counter_label_text.set(f"{self.class_frame.sample_counter} image samples")
