import tkinter as tk
from tkinter import ttk
from main_content_frames import DataFrame, TrainFrame, TestFrame

COLOUR_PRIMARY = "#2e3f4f"
COLOUR_SECONDARY = "#293846"
COLOUR_LIGHT_BACKGROUND = "#fff"
COLOUR_LIGHT_TEXT = "#eee"
COLOUR_DARK_TEXT = "#8095a8"


class AppWindow(tk.Tk):

    # The application window, contains:
    # 1. title frame at (0,0)
    # 2. main classifier frame (1,0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set general window properties
        self.geometry("1600x800")
        # self.resizable(False, False)
        self.title("image classifier")

        # set row & col config
        self.columnconfigure(0, weight=1)

        #       --style--
        style = ttk.Style(self)
        style.theme_use("clam")
        self["background"] = COLOUR_PRIMARY

        style.configure("Background1.TFrame", background=COLOUR_DARK_TEXT)
        style.configure("Background2.TFrame", background=COLOUR_LIGHT_TEXT)
        style.configure("Background3.TFrame", background=COLOUR_PRIMARY)

        #       --frames--

        # main container:
        # in: root (0,0) - contains all other frames
        # contains: (0,0) - AppTitle, (1,0) - ClassifierContainer

        container = ttk.Frame(self, style="Background1.TFrame")
        # pack the container (not grid because it is the only element in root)
        container.pack(side="top", fill="both", expand=True)
        # configure row & col
        container.columnconfigure(0, weight=1)  # expanding col 0
        container.rowconfigure(1, weight=1)  # expanding 1st row: will contain the classifier

        # title frame
        self.title_frame = AppTitle(container)
        # Classifier Container:
        self.classifier_frame = ClassifierContainer(container)


class AppTitle(ttk.Frame):

    # The application title frame,
    # contains: title label at (0,0)
    # placed in: grid (0,0) in the application window

    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        # place in AppWindow : container frame
        self.grid(row=0, column=0, padx=5, pady=10, sticky="EW")
        # expand 1st col to centralize the title label
        self.columnconfigure(0, weight=1)

        self["style"] = "Background2.TFrame"

        self.app_title_label = ttk.Label(
            self,
            text="Image Classifier",
            font=("TkDefaultFont", 20)
        )

        self.app_title_label.grid(row=0, column=0)


class ClassifierContainer(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        self["style"] = "Background2.TFrame"

        # place in AppWindow : container frame
        self.grid(row=1, column=0, padx=5, pady=10, sticky="NSEW")

        # col size config for 3 sections: data, train, test
        self.columnconfigure(0, weight=10)  # data = 10/20 of width
        self.columnconfigure(1, weight=1)  # train = 3/20 of width
        self.columnconfigure(2, weight=7)  # test = 7/10 of width
        self.rowconfigure(0, weight=1)  # expand 1st to take all available space

        data_frame = DataFrame(self, frame_title="Data:")
        data_frame.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        train_frame = TrainFrame(self, frame_title="Training:")
        train_frame.grid(row=0, column=1, padx=5, pady=5, sticky="NSEW")
        test_frame = TestFrame(self, frame_title="Test:")
        test_frame.grid(row=0, column=2, padx=5, pady=5, sticky="NSEW")


root = AppWindow()
root.mainloop()
