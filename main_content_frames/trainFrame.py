import tkinter as tk
from tkinter import ttk
import numpy as np
from .sectionFrame import SectionFrame


class TrainFrame(SectionFrame):
    def __init__(self, container: ttk.Frame, frame_title: str, **kwargs):
        super().__init__(container, frame_title, **kwargs)

        #       --training option widgets--

        # widgets main frame
        widgets_container = ttk.Frame(self, style="Background1.TFrame")
        widgets_container.columnconfigure(0, weight=1)
        widgets_container.rowconfigure(1, weight=1)
        widgets_container.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")

        # 1. training button:

        # container:
        train_button_container = ttk.Frame(widgets_container, style="Background2.TFrame")
        train_button_container.columnconfigure(0, weight=1)
        train_button_container.grid(row=0, column=0, padx=5, pady=10)

        # button:
        train_button = ttk.Button(
            train_button_container,
            text="Train model:"
        )
        train_button.grid()

        # 2. options:
        self.option_widget_list = []

        options_container = SectionFrame(widgets_container, "training options:")
        options_container.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")

        # option widgets frame
        option_widgets_frame = ttk.Frame(options_container)
        option_widgets_frame.columnconfigure(0, weight=1)
        option_widgets_frame.rowconfigure(tuple(i for i in range(4)), weight=1)
        option_widgets_frame.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")

        # option widgets:

        # 2.a epochs:
        epochs_widget = EpochsSpinboxFrame(option_widgets_frame, "epochs:")
        epochs_widget.grid(row=0, column=0, padx=5, pady=5, sticky="EW")
        self.option_widget_list.append(epochs_widget)

        # 2.b batch size:
        batch_size_widget = BatchSizeComboboxFrame(option_widgets_frame, "batch size:")
        batch_size_widget.grid(row=1, column=0, padx=5, pady=5, sticky="EW")
        self.option_widget_list.append(batch_size_widget)

        # 2.c learning rate:
        lr_widget = LRSpinboxFrame(option_widgets_frame, "learning rate:")
        lr_widget.grid(row=2, column=0, padx=5, pady=5, sticky="EW")
        self.option_widget_list.append(lr_widget)

        # 2.d reset all options:
        reset_options_widget = ResetOptionsButton(container=option_widgets_frame, widget_description="reset to defaults:", command=self.reset_options)
        reset_options_widget.grid(row=3, column=0, padx=5, pady=5, sticky="EW")

    def reset_options(self):
        # reset all option widgets to their initial value

        for widget in self.option_widget_list:
            widget.reset_option()


# a father class to all option widgets
class OptionWidgetFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, widget_description: str, **kwargs):
        super().__init__(container, **kwargs)

        # col config:
        self.columnconfigure((0, 1), weight=1)

        # description label:
        label = ttk.Label(
            self,
            text=widget_description
        )

        label.grid(row=0, column=0, padx=(10, 0), sticky="W")

    def reset_option(self):
        pass


class EpochsSpinboxFrame(OptionWidgetFrame):
    def __init__(self, container: ttk.Frame, widget_description: str, **kwargs):
        super().__init__(container, widget_description, **kwargs)

        # epochs spinbox:
        self.init_val = 25
        self.epochs_num = tk.IntVar(value=self.init_val)  # a tk int to store the selected epoch number

        self.epochs_spinbox = ttk.Spinbox(
            self,
            value=tuple([i for i in range(5, 55, 5)]),
            textvariable=self.epochs_num,
            wrap=False,
            state="readonly"
        )

        self.epochs_spinbox.grid(row=0, column=1, padx=(0, 10), sticky="E")

    def reset_option(self):
        self.epochs_num.set(self.init_val)


class LRSpinboxFrame(OptionWidgetFrame):
    def __init__(self, container: ttk.Frame, widget_description: str, **kwargs):
        super().__init__(container, widget_description, **kwargs)

        # epochs spinbox:
        self.init_val = 0.001
        self.lr = tk.DoubleVar(value=self.init_val)  # a tk int to store the selected epoch number

        self.epochs_spinbox = ttk.Spinbox(
            self,
            value=[round(i, 5) for i in np.arange(0.00001, 1, 0.00001)],
            textvariable=self.lr,
            wrap=False,
            state="readonly"
        )

        self.epochs_spinbox.grid(row=0, column=1, padx=(0, 10), sticky="E")

    def reset_option(self):
        self.lr.set(self.init_val)


class BatchSizeComboboxFrame(OptionWidgetFrame):
    def __init__(self, container: ttk.Frame, widget_description: str, **kwargs):
        super().__init__(container, widget_description, **kwargs)

        self.init_val = 32
        self.batch_size = tk.IntVar(value=self.init_val)

        self.batch_size_combobox = ttk.Combobox(
            self,
            values=tuple([2 ** i for i in range(4, 10)]),
            textvariable=self.batch_size,
            state="readonly"
        )

        self.batch_size_combobox.grid(row=0, column=1, padx=(0, 10), sticky="E")

    def reset_option(self):
        self.batch_size.set(self.init_val)


class ResetOptionsButton(OptionWidgetFrame):
    def __init__(self, container: ttk.Frame, widget_description: str, command, **kwargs):
        super().__init__(container, widget_description, **kwargs)

        self.reset_button = ttk.Button(
            self,
            text="Reset options:",
            command=command
        )

        self.reset_button.grid(row=0, column=1, padx=(0, 10), sticky="E")
