from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

from tensorflow import keras


class Brain:
    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size * 8
        self.nn_model = None
        self.__build_model()

    def get_weights(self):
        layers_weights = []
        for layer in self.nn_model.layers:
            weights = layer.get_weights()  # list of numpy arrays
            layers_weights.append(weights)
        return layers_weights

    def set_weights(self, new_weights):
        for i, layer in enumerate(self.nn_model.layers):
            layer.set_weights(new_weights[i])

    def __build_model(self) -> keras.Sequential:
        model = keras.Sequential(
            [
                keras.layers.Dense(64, activation="relu", input_dim=self.input_size),
                keras.layers.Dense(64),
                keras.layers.Dense(self.output_size, activation="sigmoid"),
            ]
        )

        optimizer = tf.keras.optimizers.RMSprop(0.001)

        model.compile(loss="mse", optimizer=optimizer, metrics=["mae", "mse"])
        model.build()
        self.nn_model = model
