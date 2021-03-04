from __future__ import annotations
import tkinter as tk
from tkinter import ttk

from main_content_frames.webcam_display import WebcamDisplayFrame

'''
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_content_frames.data_section_frames.classes_section.trainingClass import TrainingClass
'''


# the webcam section inside the dataFrame,
# contains the webcam display container, and the record and stop webcam buttons
class DataWebcamSectionFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, training_class=None, **kwargs):
        # removed type hinting from training_class because of circular import with dataWebcamSectionFrame
        # the commented importing above also solves the issue
        super().__init__(container, **kwargs)

        # row & col config:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # the class for which the webcam is displayed
        self.current_class = training_class

        #       --layout--

        # row 0: current class name label:
        # label container frame
        self.current_class_label_container = ttk.Frame(self)
        self.current_class_label_container.grid(row=0, column=0, padx=5, pady=5, sticky="EW")

        # tk.stringvar containing current class name
        self.current_class_name = tk.StringVar(value="")
        if self.current_class is not None:
            self.current_class_name.set(self.current_class.get_class_name())

        # label
        self.current_class_label = ttk.Label(
            self.current_class_label_container,
            anchor="center",
            textvariable=self.current_class_name,
            font=("TkDefaultFont", 15)
        )
        self.current_class_label.grid(row=0, column=0, sticky="NSEW")

        # row 1: webcam display (for now label)

        # container frame for webcam display: webcamDisplayFrame will be added to it
        self.webcam_display_container = ttk.Frame(self)
        self.webcam_display_container.columnconfigure(0, weight=1)
        self.webcam_display_container.rowconfigure(0, weight=1)
        self.webcam_display_container.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")

        # row 2: 'record' and 'stop webcam' buttons:

        # buttons frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.columnconfigure((0, 1), weight=1)
        buttons_frame.grid(row=2, column=0, padx=5, pady=5, sticky="EW")

        # record button:
        record_button = ttk.Button(
            buttons_frame,
            text="Record:"
        )
        # binding button press and release:
        record_button.bind('<ButtonPress-1>', self.enable_record)
        record_button.bind('<ButtonRelease-1>', self.disable_record)

        record_button.grid(row=0, column=0, padx=5, pady=5, sticky="E")

        # stop webcam button:
        stop_webcam_button = ttk.Button(
            buttons_frame,
            text="Stop webcam:",
            command=self.stop_webcam
        )
        stop_webcam_button.grid(row=0, column=1, padx=5, pady=5, sticky="W")

    # return T/F if webcam is displaying:
    def is_webcam_displayed(self) -> bool:
        # check if webcamDisplayFrame obj exists inside self.webcam_display_container:
        # using the fact that winfo_children() returns a list: empty lists are evaluated as False
        return self.webcam_display_container.winfo_children()

    # triggered by the stop webcam button
    def stop_webcam(self):
        # destroy all existing objects inside webcam_section_frame.webcam_display_container (from any other class)
        for child in self.webcam_display_container.winfo_children():
            child.destroy()

        # clear current_class_label
        self.current_class_name.set("")

    # triggeted by the record button as long as it is pressed down
    def enable_record(self, event):
        if self.is_webcam_displayed():  # only when webcam is active
            # get the webcamDisplayFrame obj from winfo_children
            webcam_display = self.webcam_display_container.winfo_children()[0]

            # set record property in webcamDisplayFrame to True
            webcam_display.set_record(True)

    # triggered when the record button is released
    def disable_record(self, event):
        if self.is_webcam_displayed():  # only when webcam is active
            # get the webcamDisplayFrame obj from winfo_children
            webcam_display = self.webcam_display_container.winfo_children()[0]

            # set record property in webcamDisplayFrame to False
            webcam_display.set_record(False)

