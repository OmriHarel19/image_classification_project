import tkinter as tk
from tkinter import ttk


# a prediction frame: will display the model prediction of the given class
class PredictionFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, class_name: str, **kwargs):
        super().__init__(container, **kwargs)

        # col config:
        self.columnconfigure((0, 1), weight=1)

        #       --properties--

        # col 0: prediction description: "{class name}: {prediction in percentage}"
        self.label_text = tk.StringVar(value=f"{class_name}: 0%")
        self.pred_label = ttk.Label(
            self,
            textvariable=self.label_text
        )
        self.pred_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        # col 1: prediction bar
        self.pred_bar = ttk.Progressbar(
            self,
            orient="horizontal",
            length=150,
            mode="determinate"  # make a continuous progress bar
        )
        self.pred_bar.grid(row=0, column=1, padx=5, pady=5, sticky="W")


