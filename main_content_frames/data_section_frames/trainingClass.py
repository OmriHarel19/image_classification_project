import tkinter as tk
from tkinter import ttk
from .classFrame import ClassFrame


# a training class object, contains the:
# classFrame, class samples and class state
class TrainingClass:
    def __init__(self, container: ttk.Frame, class_num: int, **kwargs):

        #       --properties--
        self.class_frame = ClassFrame(container=container, class_num=class_num)
        self.samples = []  # list containing class image samples
        self.enabled = True  # boolean state of the class 

