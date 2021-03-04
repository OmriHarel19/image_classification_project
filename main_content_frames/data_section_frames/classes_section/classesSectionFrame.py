from tkinter import ttk
from main_content_frames.data_section_frames.classes_section.classesWindow import ClassesWindow
from main_content_frames.data_section_frames.webcam_section.dataWebcamSectionFrame import DataWebcamSectionFrame


# a frame that contains the classes section inside the dataFrame
# contains the scrollable class window and the "add class" button.
class ClassesSectionFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, webcam_section_frame: DataWebcamSectionFrame, **kwargs):
        super().__init__(container, **kwargs)

        # row & col config:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        #       --layout--

        # row 0: scrollable classes window
        self.classes_window = ClassesWindow(self)
        self.classes_window.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

        # row 1: add class button
        # addClass button:
        add_button = ttk.Button(
            self,
            text="Add Class:",
            command=lambda: self.classes_window.add_class(webcam_section_frame)
        )
        add_button.grid(row=1, column=0, padx=5, pady=5)
