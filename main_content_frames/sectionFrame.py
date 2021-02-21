import tkinter as tk
from tkinter import ttk


# a general "father class" for any frame that has a title frame at (0,0) and the rest of its content is placed
# in (1,0)
# this class is used for the 3 main sections of the app: data, train, test
# and for the options section inside the training tab

class SectionFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, frame_title: str = "Title",  **kwargs):
        super().__init__(container, **kwargs)

        self["style"] = "Background3.TFrame"

        # col configure:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)  # 2nd row, which holds the content, takes all available space

        #       --title--
        title_frame = ttk.Frame(self, style="Background2.TFrame")
        title_frame.columnconfigure(0, weight=1)  # take all horizontal space
        title_frame.grid(row=0, column=0, padx=5, pady=5, sticky="EW")

        # title label:
        title_label = ttk.Label(
            title_frame,
            text=frame_title,
            font=("TkDefaultFont", 15)
        )
        title_label.grid(row=0, column=0)
