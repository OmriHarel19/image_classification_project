import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import os
from PIL import Image, ImageTk

import numpy as np
# import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

from main_content_frames.data_section_frames.classes_section.classFrame import ClassFrame


# a training class object, contains the:
# classFrame, class samples and class state
class TrainingClass:
    def __init__(self, container: ttk.Frame, class_num: int, **kwargs):

        #       --properties--

        self.class_frame = ClassFrame(container=container, class_num=class_num)
        self.class_frame.upload_button["command"] = self.upload_images
        self.samples = np.empty(shape=(0, 150, 150, 3))  # 4 dim array containing class image samples
        self.enabled = True  # boolean state of the class 

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
            current_samples = np.empty((len(file_paths), 150, 150, 3))

            for idx, img_path in enumerate(file_paths):

                # load img
                img = load_img(img_path, color_mode='rgb', target_size=(150, 150))
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
