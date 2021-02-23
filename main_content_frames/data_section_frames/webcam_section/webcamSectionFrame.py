import tkinter as tk
from tkinter import ttk


class WebcamSectionFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, **kwargs):
        super().__init__(container, **kwargs)

        # row & col config:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        #       --layout--

        # row 0: webcam display (for now label)

        self.display_label = ttk.Label(
            self,
            justify=tk.CENTER,
            text="Im here!",
            font=("TkDefaultFont", 15)
        )
        self.display_label.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

        # row 1: record button:

        record_button = ttk.Button(
            self,
            text="Record:"
        )
        record_button.grid(row=1, column=0, padx=5, pady=5)
