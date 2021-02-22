import tkinter as tk
from tkinter import ttk
from main_content_frames.scrollable_window import ScrollableWindow
from .trainingClass import TrainingClass


# the classes scrollable window:
class ClassesWindow(ScrollableWindow):
    def __init__(self, container: ttk.Frame, **kwargs):
        super().__init__(container, **kwargs)

        #       --properties--
        self.class_num = 1  # current class number: starts at 1, increases with every added class
        self.classes_list = []  # list of existing classes (type TrainingClass)

    # the method triggered by the "add class" button
    def addClass(self):
        new_class = TrainingClass(self.scrollable_frame, self.class_num)  # create a new class obj
        self.class_num += 1  # increase class counter
        self.classes_list.append(new_class)  # add new class to list
        new_class.class_frame.grid(padx=5, pady=20, sticky="EW")  # add new classFrame to the window

        # scroll down to the end of the scrollable area to the latest added class:
        self.after(150, lambda: self.yview_moveto(1.0))

