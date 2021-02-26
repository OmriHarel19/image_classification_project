import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from PIL import Image, ImageTk
from tensorflow.keras.preprocessing.image import load_img, img_to_array


class TestImageDisplaySectionFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, **kwargs):
        super().__init__(container, **kwargs)

        # row & col config:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # row 0: webcam & upload buttons
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.grid(row=0, column=0, padx=5, pady=5, sticky="EW")

        # webcam button:
        self.webcam_button = ttk.Button(
            self.buttons_frame,
            text="webcam"
        )
        self.webcam_button.grid(row=0, column=0, padx=2, pady=2, sticky="E")

        # upload button:
        self.upload_button = ttk.Button(
            self.buttons_frame,
            text="upload",
            command=self.upload_test_image
        )
        self.upload_button.grid(row=0, column=1, padx=2, pady=2, sticky="W")

        # row 1: image display frame: for image upload & webcam display
        self.image_display_frame = ttk.Frame(self)
        self.image_display_frame.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")

        self.display_label = ttk.Label(
            self.image_display_frame,
            justify=tk.CENTER,
            text="Im here!",
            font=("TkDefaultFont", 15)
        )
        self.display_label.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

    # upload test image from file explorer and display in image_display_frame
    def upload_test_image(self):
        # open file explorer:
        file_path = tk.filedialog.askopenfilename(  # returns a tuple of selected file paths
            initialdir=os.getcwd(),
            title="Select Image file",
            filetypes=(("JPG File", "*.jpg"), ("JPEG File", "*.jpeg"), ("PNG File", "*.png"))
        )

        if file_path != "":  # check that a file was selected
            img = Image.open(file_path)
            img.thumbnail((300, 300))
            img = ImageTk.PhotoImage(img)

            self.display_label.image = img
