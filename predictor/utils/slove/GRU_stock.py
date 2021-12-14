import numpy as np
import random
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import math
from sklearn.metrics import mean_squared_error, mean_absolute_error

def normalization_data(df, sc):
    df.astype(float)
    df['open'] = sc.fit_transform(df.open.values.reshape(-1, 1))
    df['high'] = sc.fit_transform(df.high.values.reshape(-1, 1))
    df['low'] = sc.fit_transform(df.low.values.reshape(-1, 1))
    df['volume'] = sc.fit_transform(df.volume.values.reshape(-1, 1))
    df['outstanding_share'] = sc.fit_transform(df.outstanding_share.values.reshape(-1, 1))
    df['turnover'] = sc.fit_transform(df.turnover.values.reshape(-1, 1))
    df['close'] = sc.fit_transform(df.close.values.reshape(-1, 1))
    return df


def gru_stock(model, data_raw, sqe_len, checkpoint_save_path, sc):
    test_size_percentage = 20

    x_train = []
    y_train = []

    x_test = []
    y_test = []

    test_start = round((len(data_raw) - sqe_len) * (1 - test_size_percentage / 100)) + 1

    for i in range(test_start):
        x_train.append(data_raw[i: i + sqe_len])
        y_train.append(data_raw[i + sqe_len, 3])

    for i in range(test_start, len(data_raw) - sqe_len):
        x_test.append(data_raw[i: i + sqe_len])
        y_test.append(data_raw[i + sqe_len, 3])

    seed = random.random()
    random.seed(seed)
    random.shuffle(x_train)
    random.seed(seed)
    random.shuffle(y_train)

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_test, y_test = np.array(x_test), np.array(y_test)

    x_train = np.reshape(x_train, (x_train.shape[0], sqe_len, 7))
    x_test = np.reshape(x_test, (x_test.shape[0], sqe_len, 7))

    model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
                  loss='mean_squared_error')
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_save_path + 'checkpoint.ckpt',
                                                     save_weights_only=True,
                                                     save_best_only=True,
                                                     monitor='val_loss')

    history = model.fit(x_train, y_train, batch_size=64, epochs=1, validation_data=(x_test, y_test), validation_freq=1,
              callbacks=[cp_callback])

# model.summary()

# file = open(checkpoint_save_path + 'weights.txt', 'w')
# for v in model.trainable_variables:
#     file.write(str(v.name) + '\n')
#     file.write(str(v.shape) + '\n')
#     file.write(str(v.numpy()) + '\n')
# file.close()

    loss = history.history['loss']
    val_loss = history.history['val_loss']
    plt.figure(figsize=(10, 5))
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.show()
    # sc = MinMaxScaler()
    real_stock_price = sc.inverse_transform(y_test.reshape(-1, 1))
    predicted_stock_price = sc.inverse_transform(model.predict(x_test).reshape(-1, 1))
    # real_stock_price = sc.inverse_transform(y_test)
    # predicted_stock_price = sc.inverse_transform(y_train)
    plt.plot(real_stock_price, color='red', label='Stock Price')
    plt.plot(predicted_stock_price, color='blue', label='Predicted Stock Price')
    plt.title('Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

    mse = mean_squared_error(predicted_stock_price, real_stock_price)
    rmse = math.sqrt(mean_squared_error(predicted_stock_price, real_stock_price))
    mae = mean_absolute_error(predicted_stock_price, real_stock_price)
    print('均方误差: %.6f' % mse)
    print('均方根误差: %.6f' % rmse)
    print('平均绝对误差: %.6f' % mae)
