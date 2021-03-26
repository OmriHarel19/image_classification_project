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
        self.class_name = tk.StringVar(value=f"Class {class_num}")

        self.class_name_entry = ttk.Entry(
            self,
            width=15,
            textvariable=self.class_name,
        )

        self.class_name_entry.grid(row=0, column=0, padx=2, pady=2, sticky="W")

        # options combobox:
        self.current_option = tk.StringVar()
        self.options_combobox = ttk.Combobox(
            self,
            values=("delete class", "disable class", "enable class", "delete all samples"),
            state="readonly",
            textvariable=self.current_option
        )
        self.options_combobox.grid(row=0, column=1, padx=2, pady=2, sticky="E")

        # 2nd row: separator
        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky="EW")

        # 3rd row: "x image samples" label, and class state label:

        self.class_state_label_text = tk.StringVar(value="class enabled")
        self.class_state_label = ttk.Label(
            self,
            textvariable=self.class_state_label_text,
            foreground="red",
            font=("TkDefaultFont", 10)
        )
        self.class_state_label.grid(row=2, column=1, padx=2, pady=2)

        self.sample_counter_label_text = tk.StringVar(value=f"0 image samples")

        self.sample_counter_label = ttk.Label(
            self,
            textvariable=self.sample_counter_label_text,
            foreground="blue",
            font=("TkDefaultFont", 10)
        )
        self.sample_counter_label.grid(row=2, column=0, padx=2, pady=2)

        # 4th row: collect data buttons:

        # webcam button:
        self.webcam_button = ttk.Button(
            self,
            text="webcam"
        )
        self.webcam_button.grid(row=3, column=0, padx=2, pady=2, sticky="EW")

        # upload button:
        self.upload_button = ttk.Button(
            self,
            text="upload"
        )
        self.upload_button.grid(row=3, column=1, padx=2, pady=2, sticky="EW")
