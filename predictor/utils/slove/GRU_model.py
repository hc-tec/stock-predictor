import tensorflow as tf
from tensorflow.python.keras.layers import GRU, Dropout, Dense


def get_gru_model():
    return tf.keras.Sequential([
        GRU(80, return_sequences=True),
        Dropout(0.2),
        GRU(100),
        Dropout(0.2),
        Dense(1)
    ])
