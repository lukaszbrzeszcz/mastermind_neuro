from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

from tensorflow import keras


def build_model(input_dim, output_data_size) -> keras.Sequential:
    model = keras.Sequential(
        [
            keras.layers.Dense(16, activation="relu", input_dim=input_dim),
            keras.layers.Dense(output_data_size, activation="sigmoid"),
        ]
    )

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss="mse", optimizer=optimizer, metrics=["mae", "mse"])
    model.build()
    return model
