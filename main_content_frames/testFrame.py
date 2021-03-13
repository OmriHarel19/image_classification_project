import tkinter as tk
from tkinter import ttk
from .sectionFrame import SectionFrame
from main_content_frames.test_section_frames import TestImageDisplaySectionFrame, PredictionDisplayFrame
from main_content_frames.train_section.mobileNetModel import MnetModel


class TestFrame(SectionFrame):
    def __init__(self, container: ttk.Frame, frame_title: str, **kwargs):
        super().__init__(container, frame_title, **kwargs)

        #       --properties--
        self.test_main_frame = ttk.Frame(self, style="Background1.TFrame")

        # row & col config: first row takes twice as much space as the second row
        self.test_main_frame.columnconfigure(0, weight=1)
        self.test_main_frame.rowconfigure(0, weight=1)
        # self.test_main_frame.rowconfigure(0, weight=4)
        # self.test_main_frame.rowconfigure(1, weight=1)

        self.test_main_frame.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")

        # prediction display frame:
        self.pred_display_frame = PredictionDisplayFrame(container=self.test_main_frame, frame_title="Predictions:")
        self.pred_display_frame.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")

        # image display frame
        self.image_display_frame = TestImageDisplaySectionFrame(container=self.test_main_frame, predictions_window=self.pred_display_frame.pred_window)
        self.image_display_frame.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

    # triggered by the train model button (in TrainFrame)
    def start_testing(self, trained_classifier: MnetModel):
        # enable buttons:
        for button in self.image_display_frame.buttons_list:
            button["state"] = "normal"

        # create prediction frames for each class
        self.pred_display_frame.pred_window.create_prediction_frames(trained_classifier)

        # give the model to image_display_frame (for later testing of the model)
        self.image_display_frame.set_trained_classifier(trained_classifier)
