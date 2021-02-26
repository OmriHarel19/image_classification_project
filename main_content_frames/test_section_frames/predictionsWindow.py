from tkinter import ttk
from main_content_frames.scrollable_window import ScrollableWindow
from .predictionFrame import PredictionFrame


# a scrollable window that will contain the predictions (frame objects: PredictionFrame) of each class
class PredictionsWindow(ScrollableWindow):
    def __init__(self, container: ttk.Frame, **kwargs):
        super().__init__(container, **kwargs)

        #       --properties--
        self.predictions_frames = []  # list that will contain all prediction objects

        # add prediction frames to the prediction window:
        for i in range(15):
            pred_frame = PredictionFrame(container=self.scrollable_frame, class_name=f"class {i}")
            pred_frame.pack(side="top", padx=5, pady=10, expand=True, fill="x")
            self.predictions_frames.append(pred_frame)
