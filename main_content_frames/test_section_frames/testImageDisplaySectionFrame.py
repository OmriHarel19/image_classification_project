import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from PIL import Image, ImageTk
from tensorflow.keras.preprocessing.image import load_img, img_to_array

from main_content_frames.webcam_display import *


class TestImageDisplaySectionFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, **kwargs):
        super().__init__(container, **kwargs)

        self.upload_img = None

        # row & col config:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # row 0: webcam & upload buttons
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.grid(row=0, column=0, padx=5, pady=5, sticky="EW")

        # webcam button:
        self.webcam_button = ttk.Button(
            self.buttons_frame,
            text="webcam",
            command=self.webcam_display
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
        # contains both display label for upload and display canvas for webcam
        # switching frame with tkraise()

        self.image_display_frame = ttk.Frame(self, style="Background1.TFrame")
        self.image_display_frame.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")

        # webcam display canvas

        self.webcam_display_container = ttk.Frame(self)
        self.webcam_display_container.columnconfigure(0, weight=1)
        self.webcam_display_container.rowconfigure(0, weight=1)
        self.webcam_display_container.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")

        # upload display label
        self.display_label_container = ttk.Frame(self)
        self.display_label_container.columnconfigure(0, weight=1)
        self.display_label_container.rowconfigure(0, weight=1)
        self.display_label_container.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")

        self.display_label = ttk.Label(
            self.display_label_container,
            anchor="center",
            text="image testing display",
            font=("TkDefaultFont", 15),
        )
        self.display_label.pack(expand=True, fill="both", padx=5, pady=5)
        ''''''

    # upload test image from file explorer and display in image_display_frame
    def upload_test_image(self):
        # destroy all existing objects inside webcam_display_container
        for child in self.webcam_display_container.winfo_children():
            child.destroy()

        # open file explorer:
        file_path = tk.filedialog.askopenfilename(  # returns a tuple of selected file paths
            initialdir=os.getcwd(),
            title="Select Image file",
            filetypes=(("JPG File", "*.jpg"), ("JPEG File", "*.jpeg"), ("PNG File", "*.png"))
        )

        if file_path != "":  # check that a file was selected
            # load image
            self.upload_img = Image.open(file_path)
            print("Image.open: ", type(self.upload_img))
            self.upload_img.thumbnail((300, 300))
            self.upload_img = ImageTk.PhotoImage(self.upload_img)
            # put on label
            self.display_label.configure(image=self.upload_img)
            self.display_label.image = self.upload_img

            # raise frame
            self.display_label_container.tkraise()

    # display webcam footage in image_display_frame
    def webcam_display(self):
        # destroy all existing objects inside webcam_section_frame.webcam_display_container (from any other class)

        try:
            # create WebcamDisplayFrame inside image_display_frame
            webcam_display = WebcamDisplayFrame(self.webcam_display_container, video_source=0)
            webcam_display.grid(row=0, column=0, sticky="NSEW")

            # raise frame
            self.webcam_display_container.tkraise()

        except ValueError:
            self.display_label["text"] = "no video source detected"
