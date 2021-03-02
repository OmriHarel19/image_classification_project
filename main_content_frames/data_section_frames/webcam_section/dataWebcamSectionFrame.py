import tkinter as tk
from tkinter import ttk

from main_content_frames.webcam_display import WebcamDisplayFrame


class DataWebcamSectionFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, class_name: str, **kwargs):
        super().__init__(container, **kwargs)

        # row & col config:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        #       --layout--

        # row 0: current class name label:
        self.current_class_label = ttk.Label(
            self,
            justify=tk.CENTER,
            text=class_name,
            font=("TkDefaultFont", 15)
        )
        self.current_class_label.grid(row=0, column=0, padx=5, pady=5, sticky="EW")

        # row 1: webcam display (for now label)

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
        record_button.grid(row=0, column=0, padx=5, pady=5, sticky="E")

        # stop webcam button:
        stop_webcam_button = ttk.Button(
            buttons_frame,
            text="Stop webcam:",
            command=self.stop_webcam
        )
        stop_webcam_button.grid(row=0, column=1, padx=5, pady=5, sticky="W")

    def stop_webcam(self):
        # destroy all existing objects inside webcam_section_frame.webcam_display_container (from any other class)
        for child in self.webcam_display_container.winfo_children():
            child.destroy()
