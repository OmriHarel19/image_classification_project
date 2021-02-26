import tkinter as tk
from tkinter import ttk
from main_content_frames.sectionFrame import SectionFrame
from .predictionsWindow import PredictionsWindow


# the predictions sections inside the test section, contains the predictions window
class PredictionDisplayFrame(SectionFrame):
    def __init__(self, container: ttk.Frame, frame_title: str, **kwargs):
        super().__init__(container, frame_title, **kwargs)

        #       -properties--
        self.pred_window_container = ttk.Frame(self)
        self.pred_window_container.columnconfigure(0, weight=1)
        self.pred_window_container.rowconfigure(0, weight=1)
        self.pred_window_container.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")

        self.pred_window = PredictionsWindow(self.pred_window_container)
        self.pred_window.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
