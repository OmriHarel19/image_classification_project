import tkinter as tk
from tkinter import ttk
from .sectionFrame import SectionFrame


class TestFrame(SectionFrame):
    def __init__(self, container: ttk.Frame, frame_title: str,  **kwargs):
        super().__init__(container, frame_title, **kwargs)

