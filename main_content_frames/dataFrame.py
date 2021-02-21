import tkinter as tk
from tkinter import ttk
from .sectionFrame import SectionFrame
from .data_section_frames import ClassFrame
from .scrollable_window import ScrollableWindow


class DataFrame(SectionFrame):
    def __init__(self, container: ttk.Frame, frame_title: str, **kwargs):
        super().__init__(container, frame_title, **kwargs)

        #       --(classes & webcam collect data) container--
        data_main_frame = ttk.Frame(self, style="Background1.TFrame")
        # data_main_frame.columnconfigure((0, 1), weight=1)  # split the frame equally between the classes % webcam frames

        # some bug with the splitting, meanwhile row 1 (of the webcam gets all available space)
        data_main_frame.columnconfigure(1, weight=1)  # split the frame equally between the classes % webcam frames
        data_main_frame.rowconfigure(0, weight=1)
        data_main_frame.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")  # expand in both axis

        # classes container:
        classes_container = ttk.Frame(data_main_frame, style="Background3.TFrame")
        # classes_container.columnconfigure(0, weight=1)  # take all horizontal space
        classes_container.rowconfigure(0, weight=1)  # 1st row, which holds the content, takes all available space
        classes_container.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

        # webcam container:
        webcam_container = ttk.Frame(data_main_frame, style="Background3.TFrame")
        webcam_container.columnconfigure(0, weight=1)  # take all horizontal space
        webcam_container.rowconfigure(0, weight=1)  # 1st row, which holds the content, takes all available space
        webcam_container.grid(row=0, column=1, padx=5, pady=5, sticky="NSEW")

        # scrollable classes window
        classes_window = ScrollableWindow(classes_container)
        classes_window.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

        for i in range(15):
            ClassFrame(classes_window.scrollable_frame, class_num=i).pack(side="top")

        '''
        class_example1 = ClassFrame(classes_window.scrollable_frame, class_num=1)
        class_example1.pack(side="top")
        class_example2 = ClassFrame(classes_window.scrollable_frame, class_num=2)
        class_example2.pack(side="top")

        
        # classes frame
        classes_frame = ttk.Frame(classes_container)
        classes_frame.grid(row=0, column=0, padx=5, pady=5, sticky="EW")
        
        class_example1 = ClassFrame(classes_frame, class_num=1)
        class_example1.pack(side="top")
        class_example2 = ClassFrame(classes_frame, class_num=2)
        class_example2.pack(side="top")

        # "add class" button frame:
        add_button_frame = ttk.Frame(classes_container)
        add_button_frame.columnconfigure(0, weight=1)
        add_button_frame.grid(row=1, column=0, padx=5, pady=5, sticky="EW")

        # addClass button:
        add_button = ttk.Button(
            add_button_frame,
            text="Add Class:",
        )
        add_button.grid(row=1, column=0)
        '''
