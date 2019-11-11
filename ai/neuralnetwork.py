from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

from tensorflow import keras


def build_model(input_data, output_data_size):
    model = keras.Sequential(
        [
            keras.layers.Dense(
                len(input_data), activation="relu", input_shape=input_data
            ),
            keras.layers.Dense(64, activation="relu"),
            keras.layers.Dense(output_data_size),
        ]
    )

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss="mse", optimizer=optimizer, metrics=["mae", "mse"])
    model.build()
    return model
