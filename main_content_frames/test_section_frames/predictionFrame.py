import tkinter as tk
from tkinter import ttk


# a prediction frame: will display the model prediction of the given class
class PredictionFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, class_name: str, **kwargs):
        super().__init__(container, **kwargs)

        # col config:
        self.columnconfigure((0, 1), weight=1)

        #       --properties--

        self.class_name = class_name
        # the prediction value in percentage, variable of the progress bar
        self.prediction = tk.IntVar(value=0)
        # class nae and prediction in percentage, variable of the label
        self.label_text = tk.StringVar(value=f"{self.class_name}: {self.prediction.get()}%")

        # col 0: prediction description: "{class name}: {prediction in percentage}"

        self.pred_label = ttk.Label(
            self,
            textvariable=self.label_text
        )
        self.pred_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        # col 1: prediction bar

        self.pred_bar = ttk.Progressbar(
            self,
            variable=self.prediction,
            orient="horizontal",
            length=150,
            mode="determinate"  # make a continuous progress bar
        )
        self.pred_bar.grid(row=0, column=1, padx=5, pady=5, sticky="W")

    def set_prediction(self, pred: float):
        self.prediction.set(round(pred * 100))
        self.label_text.set(f"{self.class_name}: {self.prediction.get()}%")

    def get_class_name(self):
        return self.class_name
