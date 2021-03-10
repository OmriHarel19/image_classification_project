import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf

# imports for model:
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras import regularizers


class MnetModel:
    def __init__(self, train_data: np.array, train_labels: np.array, epochs: int, batch_size: int, lr: float):
        # properties:
        self.data = train_data
        self.labels = train_labels
        self.model = None

        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr

        # 1. pre-process
        for i in range(self.data.shape[0]):
            self.data[i] = preprocess_input(self.data[i])

        # 2. split to train & test sets (also shuffles the data set)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.data, self.labels, test_size=0.3, shuffle=True)

        # 3. create model
        self.create_model()

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
            Dense(1, activation='sigmoid')  # add the binary classification layer
        ])

        # freeze the pre-trained weights of mnet:
        complete_model.layers[0].trainable = False

        # compile:
        complete_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        self.model = complete_model

    def train_model(self):
        steps_per_epoch = len(self.x_train) // self.batch_size
        validation_steps = len(self.x_test) // self.batch_size

        _ = self.model.fit_generator(
            self.data_generator("train"),
            validation_data=self.data_generator("test"),
            steps_per_epoch=steps_per_epoch,
            validation_steps=validation_steps,
            epochs=5
        )

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

    def display_predictions(self, test_batch, test_labels):

        predictions = self.model.predict(test_batch)

        for i in range(len(test_labels)):
            real_label = np.squeeze(test_labels[i])
            pred = float(np.squeeze(predictions[i]))
            print(f"real is: {real_label}, predicted is: {pred}")
