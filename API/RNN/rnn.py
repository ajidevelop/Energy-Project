__author__ = 'LobaAjisafe'

import os
import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

TRAIN_SPLIT = .8

# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def build_dataset():
    global TRAIN_SPLIT
    RNN = os.path.dirname(os.path.abspath(__file__))

    df = pd.DataFrame()
    for file in os.listdir(os.path.join(RNN, 'data')):
        if 'temp' in file:
            continue
        df1 = pd.read_csv(RNN + '\\data\\' + file)
        df = df.append(df1, ignore_index=True)

    df1 = pd.read_csv(RNN + '\\data\\temp_nov-mar.csv')
    df = pd.merge(df1.iloc[:, 1:], df, on='DateTime')

    df = df.loc[df['This Month'] != 0]  # remove rows with all zeros in dataframe
    df = df.sort_values(df.columns[0], ascending=True)

    TRAIN_SPLIT = int(np.ceil(TRAIN_SPLIT * len(df)))
    return df


all_data = build_dataset()
features = ['Temp', 'Wind', 'Humidity', 'Barometer', 'Visibility', 'Last Month', 'This Month']
features = all_data[features]
features.index = all_data['DateTime']
features.plot(subplots=True)
# plt.show()

dataset = features.values
data_mean = dataset[:TRAIN_SPLIT].mean(axis=0)
data_std = dataset[:TRAIN_SPLIT].std(axis=0)

dataset = (dataset - data_mean) / data_std


def parse_data(dataset, target, start_index, end_index, history_size, target_size, step, single_step=False):
    data = []
    labels = []

    start_index = start_index + history_size
    if end_index is None:
        end_index = len(dataset) - target_size

    assert end_index > start_index

    for i in range(start_index, end_index):
        indices = range(i - history_size, i, step)
        data.append((dataset[indices]))

        if single_step:
            labels.append(target([i+target_size]))
        else:
            labels.append(target[i:i+target_size])

    return np.array(data), np.array(labels)


future_target = 1
past_history = 300
STEP = 6
x_train_multi, y_train_multi = parse_data(dataset, dataset[:, 1], 0, TRAIN_SPLIT, past_history, future_target, STEP)
x_val_multi, y_val_multi = parse_data(dataset, dataset[:, 1], TRAIN_SPLIT, None, past_history, future_target, STEP)

BATCH_SIZE = 256
BUFFER_SIZE = 10000
EVALUATION_INTERVAL = 200
EPOCHS = 50

train_data_multi = tf.data.Dataset.from_tensor_slices((x_train_multi, y_train_multi))
train_data_multi = train_data_multi.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()

val_data_multi = tf.data.Dataset.from_tensor_slices((x_val_multi, y_val_multi))
val_data_multi = val_data_multi.batch(BATCH_SIZE).repeat()


def create_time_steps(length):
    return list(range(-length, 0))


def multi_step_plot(history, true_future, prediction):
    plt.figure(figsize=(12, 6))
    num_in = create_time_steps(len(history))
    num_out = len(true_future)

    plt.plot(num_in, np.array(history[:, 1]), label='History')
    plt.plot(np.arange(num_out)/STEP, np.array(true_future), 'bo',
             label='True Future')
    if prediction.any():
        plt.plot(np.arange(num_out)/STEP, np.array(prediction), 'ro',
                 label='Predicted Future')
    plt.legend(loc='upper left')
    plt.show()


# for x, y in train_data_multi.take(1):
#     multi_step_plot(x[0], y[0], np.array([0]))


multi_step_model = tf.keras.models.Sequential()
multi_step_model.add(tf.keras.layers.LSTM(32, return_sequences=True, input_shape=x_train_multi.shape[-2:]))
multi_step_model.add(tf.keras.layers.LSTM(16, activation='relu'))
multi_step_model.add(tf.keras.layers.Dense(future_target))

multi_step_model.compile(optimizer=tf.keras.optimizers.RMSprop(clipvalue=1.0), loss='mae')

multi_step_history = multi_step_model.fit(train_data_multi, epochs=EPOCHS,
                                          steps_per_epoch=EVALUATION_INTERVAL,
                                          validation_data=val_data_multi,
                                          validation_steps=50)


def plot_train_history(history, title):
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(loss))

    plt.figure()

    plt.plot(epochs, loss, 'b', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title(title)
    plt.legend()

    plt.show()


plot_train_history(multi_step_history, 'Multi-Step Training and validation loss')

for x, y in val_data_multi.take(3):
    multi_step_plot(x[0], y[0], multi_step_model.predict(x)[0])
