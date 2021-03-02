import tkinter as tk
from tkinter import ttk
from .sectionFrame import SectionFrame
from main_content_frames.data_section_frames import ClassesSectionFrame
from main_content_frames.data_section_frames.webcam_section import DataWebcamSectionFrame


class DataFrame(SectionFrame):
    def __init__(self, container: ttk.Frame, frame_title: str, **kwargs):
        super().__init__(container, frame_title, **kwargs)

        #       --(classes & webcam collect data) container--
        data_main_frame = ttk.Frame(self, style="Background1.TFrame")
        # data_main_frame.columnconfigure((0, 1), weight=1)  # split the frame equally between the classes % webcam frames

        # some bug with the splitting, meanwhile col 1 (of the webcam) gets all available space
        data_main_frame.columnconfigure((0, 1), weight=1)
        data_main_frame.rowconfigure(0, weight=1)
        data_main_frame.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")  # expand in both axis

        # webcam container:
        webcam_container = DataWebcamSectionFrame(data_main_frame, " ", style="Background3.TFrame")
        webcam_container.grid(row=0, column=1, padx=5, pady=5, sticky="NSEW")

        # classes section container:
        classes_section_frame = ClassesSectionFrame(data_main_frame, webcam_container)
        classes_section_frame.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")


