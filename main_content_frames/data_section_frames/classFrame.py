import tkinter as tk
from tkinter import ttk


# a frame for a class in the image classifier,
# contains the upload and webcam buttons

class ClassFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, class_num: int, **kwargs):
        super().__init__(container, **kwargs)

        self["style"] = "Background1.TFrame"

        # col config:
        self.columnconfigure((0, 1), weight=1)

        #       --layout--

        # 1st row: class name textbox & and options combobox

        # class name textbox:
        self.class_name = f"Class {class_num}"
        self.class_name_textbox = tk.Text(
            self,
            height=1,  # height in lines
            width=15,  # width in characters
            padx=3,
            state="normal"  # can be edited
        )
        self.class_name_textbox.insert("1.0", self.class_name)

        self.class_name_textbox.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        # options combobox:
        self.options_combobox = ttk.Combobox(
            self,
            values=("delete class", "disable class", "enable class", "download samples"),
            state="readonly"
        )

        self.options_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="E")

        # 2nd row: collect data buttons:

        # webcam button:
        self.webcam_button = ttk.Button(
            self,
            text="webcam"
        )
        self.webcam_button.grid(row=1, column=0, padx=2, pady=2, sticky="EW")

        # upload button:
        self.upload_button = ttk.Button(
            self,
            text="upload"
        )
        self.upload_button.grid(row=1, column=1, padx=2, pady=2, sticky="EW")
