from tkinter import ttk
from main_content_frames.scrollable_window import ScrollableWindow
from .predictionFrame import PredictionFrame
from main_content_frames.train_section.mobileNetModel import MnetModel


# a scrollable window that will contain the predictions (frame objects: PredictionFrame) of each class
class PredictionsWindow(ScrollableWindow):
    def __init__(self, container: ttk.Frame, **kwargs):
        super().__init__(container, **kwargs)

        #       --properties--
        self.prediction_frames = []  # list that will contain all prediction objects

    def create_prediction_frames(self, trained_model: MnetModel):
        # destroy all existing predictionFrames
        for child in self.scrollable_frame.winfo_children():
            child.destroy()

        # delete the prediction_frames list by making it an empty list:
        self.prediction_frames = []

        # create new predictions_frames for all classes of the model
        classes_names = trained_model.get_classes_names()

        for class_name in classes_names:
            pred_frame = PredictionFrame(container=self.scrollable_frame, class_name=class_name)
            pred_frame.pack(side="top", padx=5, pady=10, expand=True, fill="x")
            self.prediction_frames.append(pred_frame)
