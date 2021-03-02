from tkinter import ttk
from main_content_frames.scrollable_window import ScrollableWindow
from main_content_frames.data_section_frames.classes_section.trainingClass import TrainingClass
from main_content_frames.data_section_frames.webcam_section.dataWebcamSectionFrame import DataWebcamSectionFrame


# the classes scrollable window:
class ClassesWindow(ScrollableWindow):
    def __init__(self, container: ttk.Frame, **kwargs):
        super().__init__(container, **kwargs)

        #       --properties--
        self.class_num = 1  # current class number: starts at 1, increases with every added class
        self.classes_list = []  # list of existing classes (type TrainingClass)

    # the method triggered by the "add class" button
    def addClass(self, webcam_section_frame: DataWebcamSectionFrame):
        new_class = TrainingClass(container=self.scrollable_frame, class_num=self.class_num, webcam_section_frame=webcam_section_frame)  # create a new class obj
        self.class_num += 1  # increase class counter
        self.classes_list.append(new_class)  # add new class to list
        new_class.class_frame.grid(padx=5, pady=20, sticky="EW")  # add new classFrame to the window

        # scroll down to the end of the scrollable area to the latest added class:
        self.after(150, lambda: self.yview_moveto(1.0))

