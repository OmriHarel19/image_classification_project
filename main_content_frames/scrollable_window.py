import tkinter as tk
from tkinter import ttk


# Scrollable window class with tk.Canvas
class ScrollableWindow(tk.Canvas):
    def __init__(self, container: ttk.Frame, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        # create the scrollable frame
        self.scrollable_frame = ttk.Frame(self)
        self.scrollable_frame.columnconfigure(0, weight=1)  # we want the scrollable frame to take all available space

        # create the scrollable window
        self.scrollable_window = self.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # configure scroll region method - will be triggered by "<Configure>" event for the scrollable_frame
        def configure_scroll_region(event):
            self.configure(scrollregion=self.bbox("all"))

        # bind the scrollable frame to the configuration method:
        # whenever the scrollable frame size changes (<Configure> event) the method is called
        self.scrollable_frame.bind("<Configure>", configure_scroll_region)

        # enable scrolling with mouse wheel
        def on_mousewheel(event):
            self.yview_scroll(-int(event.delta / 120), "units")

        # bind <MouseWheel> event to on_mousewheel
        self.bind("<MouseWheel>", on_mousewheel)

        # create the scroll bar:
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)  # bind scrollbar to canvas yview
        scrollbar.grid(row=0, column=1, sticky="NS")  # expand vertically

        # bind canvas to the scroll bar
        self.configure(yscrollcommand=scrollbar.set)
        self.yview_moveto(1.0)
