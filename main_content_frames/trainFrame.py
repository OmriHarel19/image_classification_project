import tkinter as tk
from tkinter import ttk
import numpy as np
from .sectionFrame import SectionFrame
from main_content_frames.data_section_frames.classes_section.classesWindow import ClassesWindow
from main_content_frames.data_section_frames.classes_section.trainingClass import TrainingClass
from main_content_frames.train_section.mobileNetModel import MnetModel

from typing import Union, List


class TrainFrame(SectionFrame):
    def __init__(self, container: ttk.Frame, frame_title: str, classes_window: ClassesWindow, **kwargs):
        super().__init__(container, frame_title, **kwargs)

        self.classifier = None

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
            text="Train model:",
            command=lambda: self.train_model(classes_window.classes_list)
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

        # --option widgets--

        # 2.a epochs spinbox:
        epochs_widget_frame = OptionWidgetFrame(option_widgets_frame, widget_description="epochs:",
                                                init_val=25)  # create OptionWidgetFrame
        # create the widget, inside the OptionWidgetFrame
        epochs_widget = ttk.Spinbox(
            epochs_widget_frame,
            value=tuple([i for i in range(5, 55, 5)]),
            wrap=False,
            state="readonly"
        )
        # add the widget to the OptionWidgetFrame, widget textvariable is added in this method
        epochs_widget_frame.add_widget(epochs_widget)
        # add widget frame to the list
        self.option_widget_list.append(epochs_widget_frame)

        epochs_widget_frame.grid(row=0, column=0, padx=5, pady=5, sticky="EW")

        # 2.b batch size combobox:
        batch_size_widget_frame = OptionWidgetFrame(option_widgets_frame, widget_description="batch size:", init_val=32)

        batch_size_widget = ttk.Combobox(
            batch_size_widget_frame,
            values=tuple([2 ** i for i in range(4, 10)]),
            state="readonly"
        )

        batch_size_widget_frame.add_widget(batch_size_widget)
        self.option_widget_list.append(batch_size_widget_frame)
        batch_size_widget_frame.grid(row=1, column=0, padx=5, pady=5, sticky="EW")

        # 2.c learning rate spinbox:
        lr_widget_frame = OptionWidgetFrame(option_widgets_frame, widget_description="learning rate:", init_val=0.001)

        lr_widget = ttk.Spinbox(
            lr_widget_frame,
            value=[round(i, 5) for i in np.arange(0.00001, 1, 0.00001)],
            wrap=False,
            state="readonly"
        )

        lr_widget_frame.add_widget(lr_widget)
        self.option_widget_list.append(lr_widget_frame)
        lr_widget_frame.grid(row=2, column=0, padx=5, pady=5, sticky="EW")

        # 2.d reset options button
        reset_button_frame = ResetOptionsButton(option_widgets_frame, self.reset_options)

        reset_button_frame.grid(row=3, column=0, padx=5, pady=5, sticky="EW")

        # previous option widget implementation:
        '''
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
        '''

    def reset_options(self):
        # reset all option widgets to their initial value

        for widget in self.option_widget_list:
            widget.reset_option()

    # triggered by the train model button
    def train_model(self, classes_list: List[TrainingClass]):
        # 1. at least two training classes - done
        # 2. each class contains at least x samples (x to be decided) - not done

        if len(classes_list) >= 2:
            # create train_data np array
            sample_arrays = [training_class.samples for training_class in classes_list]
            train_data = np.concatenate(sample_arrays, axis=0)

            '''
            total_sample_count = 0
            sample_counter = 0
            train_data = np.empty((total_sample_count,))
            for sample_array in range(sample_arrays):
                for i in range(len(sample_array)):
                    train_data[sample_counter] = sample_array[i]
                    sample_counter += 1
            '''

            # create train_labels np array:
            train_labels = []
            for class_label, sample_array in enumerate(sample_arrays):
                for i in range(sample_array.shape[0]):
                    train_labels.append(class_label)
            print(f"train_labels as a normal list: {train_labels}")

            train_labels = np.array(train_labels)[:, np.newaxis]
            print(f"converting to np array: {train_labels.shape}")

            # build & trained classifier:
            self.classifier = MnetModel(train_data, train_labels, epochs=1, batch_size=16, lr=0.001)  # instantiate the model
            self.classifier.train_model()  # train

            # test the trained model
            self.classifier.display_predictions(*self.classifier.get_random_batch("test"))
        else:
            print("need at least two training classes!")


# a frame containing a label and an option widget:
class OptionWidgetFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame, widget_description: str, init_val, **kwargs):
        super().__init__(container, **kwargs)

        # option widget: initialized not defined, needs to be added to to the frame
        self.option_widget = None

        # col config:
        self.columnconfigure((0, 1), weight=1)

        # properties:
        self.init_widget_val = str(init_val)  # store value as a string
        self.widget_val = tk.StringVar(value=self.init_widget_val)

        # description label: (0,0)
        label = ttk.Label(
            self,
            text=widget_description
        )

        label.grid(row=0, column=0, padx=(10, 0), sticky="W")

    # reset option to init_val
    def reset_option(self):
        self.widget_val.set(self.init_widget_val)

    # add option widget:
    def add_widget(self, option_widget: Union[ttk.Combobox, ttk.Spinbox]):
        # option widget: (0,1)
        self.option_widget = option_widget
        self.option_widget["textvariable"] = self.widget_val  # add textvariable to the widget
        self.option_widget.grid(row=0, column=1, padx=(0, 10), sticky="E")


''' all specific WidgetFrame classes
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

        self.lr_spinbox = ttk.Spinbox(
            self,
            value=[round(i, 5) for i in np.arange(0.00001, 1, 0.00001)],
            textvariable=self.lr,
            wrap=False,
            state="readonly"
        )

        self.lr_spinbox.grid(row=0, column=1, padx=(0, 10), sticky="E")

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
'''


class ResetOptionsButton(ttk.Frame):
    def __init__(self, container: ttk.Frame, command, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=1)

        self.reset_button = ttk.Button(
            self,
            text="Reset options:",
            command=command
        )

        self.reset_button.grid(row=0, column=0)
