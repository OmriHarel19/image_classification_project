import tkinter as tk
from tkinter import ttk

from main_content_frames.webcam_display import WebcamDisplayFrame


class DataWebcamSectionFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, **kwargs):
        super().__init__(container, **kwargs)

        # row & col config:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        #       --layout--

        # row 0: webcam display (for now label)

        webcam_display = WebcamDisplayFrame(self, video_source=0)
        webcam_display.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        '''

        self.display_label = ttk.Label(
            self,
            justify=tk.CENTER,
            text="Im here!",
            font=("TkDefaultFont", 15)
        )
        self.display_label.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        '''
        # row 1: 'record' and 'stop webcam' buttons:

        # buttons frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.columnconfigure((0, 1), weight=1)
        buttons_frame.grid(row=1, column=0, padx=5, pady=5, sticky="EW")

        # record button:
        record_button = ttk.Button(
            buttons_frame,
            text="Record:"
        )
        record_button.grid(row=0, column=0, padx=5, pady=5, sticky="E")

        # stop webcam button:
        stop_webcam_button = ttk.Button(
            buttons_frame,
            text="Stop webcam:"
        )
        stop_webcam_button.grid(row=0, column=1, padx=5, pady=5, sticky="W")
