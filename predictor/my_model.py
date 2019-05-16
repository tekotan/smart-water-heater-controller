import tensorflow as tf
import numpy as np

import predictor.get_data as data


def get_model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(64, activation=tf.nn.elu, input_shape=(None, 96)))
    model.add(tf.keras.layers.Dense(32, activation=tf.nn.elu))
    model.add(tf.keras.layers.Dense(8, activation=tf.nn.elu))
    model.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid))
    
    optimizer = tf.keras.optimizers.Adam()
    model.compile(loss="binary_crossentropy", optimizer=optimizer, metrics=["accuracy", "mae", "mse", tf.keras.metrics.AUC(), tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])
    return model
def train(epochs, batch_size, model):
    callbacks = [
        # Write TensorBoard logs to `./logs` directory
        tf.keras.callbacks.TensorBoard(log_dir='./logs'),
        tf.keras.callbacks.ModelCheckpoint("./predictor/model_checkpoint/model_{epoch:02d}.ckpt")
    ]
    data_x, data_y = data.get_data()
    model.fit(data_x, data_y, epochs=epochs, batch_size=batch_size, callbacks=callbacks)