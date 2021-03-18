import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import tensorflow as tf
import tkinter as tk

from typing import List

# imports for model:
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras import regularizers
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.callbacks import ModelCheckpoint


class MnetModel:
    def __init__(self, train_data: np.array, train_labels: np.array, classes_names: List[str], epochs: int,
                 batch_size: int, lr: float):
        # properties:
        self.data, self.labels = shuffle(train_data, train_labels)
        self.model = None

        self.classes_names = classes_names
        self.classes_num = len(self.classes_names)

        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr

        # 1. pre-process
        for i in range(self.data.shape[0]):
            self.data[i] = preprocess_input(self.data[i])

        # 2. split to train & test sets (also shuffles the data set)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.data, self.labels, test_size=0.3,
                                                                                shuffle=True)
        print("data sets after split")
        print(f"x_train shape: {self.x_train.shape}")
        print(f"y_train shape: {self.y_train.shape}")
        print(f"x_test shape: {self.x_test.shape}")
        print(f"y_test shape: {self.y_test.shape}")

        # 3. create model
        self.create_model()

    # setters & getters:
    def get_number_of_classes(self):
        return self.classes_num

    def get_classes_names(self):
        return self.classes_names

    # --------------------------------------------------------------------------

    #   -- class methods--

    def load_mnet_model(self):
        mnet = tf.keras.applications.mobilenet_v2.MobileNetV2(
            include_top=False,  # emitting the last softmax layer of 1000 classes
            pooling='avg',  # shrinking from 4d tensor to a 2d tensor for the last FC layer
            weights='imagenet',  # load the weights trained on the imagenet dataset
            input_shape=(128, 128, 3)
        )
        return mnet

    def create_model(self):
        # create the entire model
        mnet = self.load_mnet_model()
        complete_model = Sequential([
            mnet,  # load the mnet model as the first layer
            Dropout(0.5),  # add a dropout layer
            Dense(100, activation='relu'),
            Dropout(0.3)  # add a dropout layer
        ])

        # freeze the pre-trained weights of mnet:
        complete_model.layers[0].trainable = False

        print("before adding classifier layer:")
        complete_model.summary()

        ''''''
        # create the classification layer according to the num of classes:

        # in case we have a binary model
        if self.classes_num == 2:
            # add the binary classification layer
            complete_model.add(Dense(1, activation='sigmoid'))

            # compile with binary_crossentropy:
            complete_model.compile(loss='binary_crossentropy',
                                   optimizer=Adam(learning_rate=self.lr),
                                   metrics=['accuracy'])

        # in case of multi-class model
        else:
            # add the softmax classification layer
            complete_model.add(Dense(self.classes_num, activation='softmax'))

            # compile with sparse_categorical_crossentropy:
            complete_model.compile(loss='sparse_categorical_crossentropy',
                                   optimizer=Adam(learning_rate=self.lr),
                                   metrics=['accuracy'])

        print("after adding classifier layer:")
        complete_model.summary()

        self.model = complete_model

    # creating a callback for saving model whenever validation acc improves
    def get_checkpoint_best_only(self, path):
        checkpoint = ModelCheckpoint(filepath=path, save_weights_only=False, save_best_only=True, save_freq='epoch',
                                     monitor='val_accuracy', verbose=1)
        return checkpoint

    def train_model(self, training_progress_var: tk.StringVar):
        # training progress callback:
        training_progress = TrainingProgressCallback(training_progress_var, self.epochs)
        # saving model callback:
        path = "trained_model/keras_model.h5"
        checkpoint = self.get_checkpoint_best_only(path)

        _ = self.model.fit(
            x=self.x_train,
            y=self.y_train,
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_data=(self.x_test, self.y_test),
            callbacks=[training_progress, checkpoint]
        )

    '''
    def train_model(self):
        steps_per_epoch = len(self.x_train) // self.batch_size
        validation_steps = len(self.x_test) // self.batch_size

        _ = self.model.fit_generator(
            self.data_generator("train"),
            validation_data=self.data_generator("test"),
            steps_per_epoch=steps_per_epoch,
            validation_steps=validation_steps,
            epochs=self.epochs
        )
    '''

    #       --training methods--

    # returns a random batch of size batch_size of samples from the selected data set (train / test)
    def get_random_batch(self, data_set: str):

        str_to_dataset = {"train": (self.x_train, self.y_train),
                          "test": (self.x_test, self.y_test)
                          }

        x, y = str_to_dataset[data_set]

        # create batch arrays:
        x_batch = np.zeros((self.batch_size, 128, 128, 3))
        y_batch = np.zeros((self.batch_size, 1))

        # get samples number
        total_samples_number = x.shape[0]

        # select random batch with np.random.choise
        indices = np.random.choice(range(total_samples_number - 1), self.batch_size)

        # create the random batch
        for i, index in enumerate(indices):
            x_batch[i] = x[index]
            y_batch[i] = y[index]

        return x_batch, y_batch

    # generating random data batches infinitely
    def data_generator(self, data_set: str):

        while True:
            data, labels = self.get_random_batch(data_set)
            yield data, labels

    def evaluate_model(self):
        test_loss, test_accuracy = self.model.evaluate(self.x_test, self.y_test, verbose=2)
        return test_loss, test_accuracy

    # suited only for binary model - remember to change
    def display_predictions(self, test_batch, test_labels):

        predictions = self.model.predict(test_batch)

        for i in range(len(test_labels)):
            real_label = np.squeeze(test_labels[i])
            pred = float(np.squeeze(predictions[i]))
            print(f"real is: {real_label}, predicted is: {pred}")


# create a custom callback class to update training label
class TrainingProgressCallback(Callback):

    def __init__(self, training_progress_var: tk.StringVar, total_epoch_num: int):
        self.training_progress_var = training_progress_var
        self.total_epoch_num = total_epoch_num

    # overriding callback method: updating according to training phase:

    def on_epoch_begin(self, epoch, logs=None):
        progress = f"training: {epoch + 1}/{self.total_epoch_num} epochs"  # epochs start at 0
        self.training_progress_var.set(progress)

    def on_train_end(self, logs=None):
        self.training_progress_var.set("finnished training!")
