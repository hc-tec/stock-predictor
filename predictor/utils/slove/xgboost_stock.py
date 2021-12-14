import pandas as pd
import numpy as np
import xgboost as xgb
from matplotlib import rcParams
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score, confusion_matrix, \
    classification_report
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from joblib import dump
import datetime


def plot_confusion_matrix(y_true, y_pred, labels=None,
                          normalize=False, title=None, cmap=None):
    if labels is None:
        labels = ["Sell", "Buy", "Hold"]
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=labels, yticklabels=labels,
           title=title,
           ylabel='ACTUAL',
           xlabel='PREDICTED')
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 1.5
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="snow" if cm[i, j] > thresh else "orange",
                    size=26)
    ax.grid(False)
    fig.tight_layout()
    return ax


def xgboost_stock(data, target, model, params, sqe_len, xgb_save_path):

        train = []
        test = []
        for i in range(len(data) - sqe_len):
            train.append(data[i: i + sqe_len])
            test.append(target[i + sqe_len])
        train = np.array(train)
        test = np.array(test)
        x_train, x_test, y_train, y_test = train_test_split(train, test)
        # x_train = np.array(x_train)

        x_test = x_test.reshape(x_test.shape[0], -1)
        y_test = y_test.reshape(y_test.shape[0], -1)

        x_train = x_train.reshape(x_train.shape[0], -1)
        y_train = y_train.reshape(y_train.shape[0], -1)
        search = GridSearchCV(model, params, cv=5, return_train_score=True, verbose=5, scoring='f1_macro')
        search.fit(x_train, y_train)
        model = search.best_estimator_
        print('best params: ', search.best_params_)
        print('best score: ', search.best_score_)
        history = model.fit(x_train, y_train)
        dump(model, xgb_save_path)

        # loss = history.history['loss']
        # val_loss = history.history['val_loss']
        # plt.figure(figsize=(10, 5))
        # plt.plot(loss, label='Training Loss')
        # plt.plot(val_loss, label='Validation Loss')
        # plt.title('Training and Validation Loss')
        # plt.legend()
        # plt.show()
        # sc = MinMaxScaler()
        # sc.fit_transform(data)
        # real_stock_price = y_test# .reshape(x_test.shape[0], -1)
        # predicted = model.predict_proba(x_test)
        # predicted_stock_price = predicted#.reshape(predicted.shape[0], -1)
        # plt.plot(real_stock_price, color='red', label='Stock Analysis')
        # plt.plot(predicted_stock_price, color='blue', label='Predicted Stock Analysis')
        # plt.title('Stock Analysis Prediction')
        # plt.xlabel('Time')
        # plt.ylabel('Stock Analysis')
        # plt.legend()
        # plt.show()
        predict = model.predict(x_test)
        report = classification_report(y_test, predict, target_names=['Sell', 'Buy', 'Hold'])
        print(report)
        plot_confusion_matrix(y_test, predict, title="Confusion Matrix")
        np.set_printoptions(precision=1)
        # Plot non-normalized confusion matrix
        plt.savefig('Confusion Matrix')
        plt.show()
