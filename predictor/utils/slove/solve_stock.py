import datetime
import os
import pandas as pd
import numpy as np
from joblib import load
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from .make_data import make_data, make_gru_last_sqe, make_xgb_last_sqe
from .GRU_stock import gru_stock, normalization_data
from .GRU_model import get_gru_model
from .xgboost_model import get_xgb_model
from .xgboost_stock import xgboost_stock

from stock.settings import BASE_DIR, STATIC_URL
STATIC_DIR = BASE_DIR + STATIC_URL + 'stock/'

data_path = STATIC_DIR

def plt_daily(data):
    money = data[:, 4]
    plt.plot(money, color='red', label='Stock Price')
    plt.title('Stock Price')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

def ply_financial(data):
    bar1 = data[:, 4]
    bar2 = data[:, 2]
    bar3 = data[:, 3]
    plt.plot(bar1, color='red', label='扣除非经常性损益后的每股收益(元)')
    plt.plot(bar2, color='gold', label='加权每股收益(元)')
    # plt.plot(bar3, color='gold', label='每股收益_调整后(元)')

    # plt.plot(data, color='red', label='Stock financial')
    plt.title('Stock financial')
    plt.xlabel('Time')
    plt.ylabel('Stock ply_financial')
    plt.legend()
    plt.show()

def ply_indicator(data):
    plt.plot(data[:, 2], color='red', label='pe')
    plt.title('Stock indicator')
    plt.xlabel('Time')
    plt.ylabel('Stock indicator')
    plt.legend()
    plt.show()

def need_make_data(stock_name):
    if os.path.exists(data_path + stock_name + '/last_time.txt'):
        file = open(data_path + stock_name + '/last_time.txt')
        temp = file.readline()
        if datetime.datetime.today() - datetime.datetime.strptime(temp, "%Y-%m-%d") < datetime.timedelta(days=2):
            return False
    return True


def predict_price(stock_name):
    checkpoint_path = data_path + '/checkpoint/' + stock_name + '/'
    model = get_gru_model()
    sqe_len = 15

    stock = pd.read_csv(data_path + stock_name + '/stock_zh_a_daily.csv')
    stock.pop('date')

    sc = MinMaxScaler()
    data_norm = normalization_data(stock, sc)
    data_raw = data_norm.values

    if not os.path.exists(checkpoint_path + 'checkpoint.ckpt.index'):
        gru_stock(model, data_raw, sqe_len, checkpoint_path, sc)

    model.load_weights(checkpoint_path + 'checkpoint.ckpt')

    x = make_gru_last_sqe(data_raw, sqe_len)
    predicted_stock_price = model.predict(x)

    return sc.inverse_transform(predicted_stock_price)[0]


def sell_or_buy(stock_name):
    sqe_len = 15
    xgb_path = data_path + '/checkpoint/' + stock_name + '/xgboost.joblib'
    params, model = get_xgb_model()

    stock = pd.read_csv(data_path + stock_name + '/stock_financial_analysis_indicator.csv')
    day_price = pd.read_csv(data_path + stock_name + '/stock_zh_a_daily.csv')
    stock_target = pd.read_csv(data_path + stock_name + '/stock_a_lg_indicator.csv')
    stock = stock[::-1]
    stock.reset_index()
    stock_target = stock_target[::-1]
    stock_target.reset_index()
    isnull = stock.isnull().any()

    stock = np.array(stock)
    day_price = np.array(day_price)
    stock_target = np.array(stock_target)

    data = []
    stock_id = 0
    stock_target_id = 0

    for i in day_price:
        new = []
        while stock_id + 1 < len(stock) and datetime.datetime.strptime(stock[stock_id + 1][0], "%Y-%m-%d") \
                <= datetime.datetime.strptime(i[0], "%Y-%m-%d"):
            stock_id = stock_id + 1
        new.append(i[4])
        while stock_target_id + 1 < len(stock_target) and datetime.datetime.strptime(
                stock_target[stock_target_id + 1][1],
                "%Y-%m-%d") <= datetime.datetime.strptime(
            i[0], "%Y-%m-%d"):
            stock_target_id = stock_target_id + 1
        if np.isnan(stock_target[stock_target_id][3]) or np.isnan(stock_target[stock_target_id][4]) or np.isnan(stock_target[stock_target_id][6]):
            continue
        new.append(float(stock_target[stock_target_id][3]))
        new.append(float(stock_target[stock_target_id][4]))
        new.append(float(stock_target[stock_target_id][6]))
        eta = stock[stock_id][1]
        cnt = 0
        while eta == '--':
            eta = stock[stock_id + cnt][1]
            cnt = cnt + 1
        new.append(float(eta))
        dar = stock[stock_id][61]
        cnt = 0
        while dar == '--':
            dar = stock[stock_id + cnt][61]
            cnt = cnt + 1
        new.append(float(dar))
        flow = stock[stock_id][61]
        cnt = 0
        while flow == '--':
            flow = stock[stock_id + cnt][61]
            cnt = cnt + 1
        new.append(float(flow))
        roe = stock[stock_id][61]
        cnt = 0
        while roe == '--':
            roe = stock[stock_id + cnt][61]
            cnt = cnt + 1
        new.append(float(roe))
        new.append(2)

        data.append(new)

    temp = []
    for i in range(0, len(data)):
        if i % 5 == 0:
            temp.append(data[i])
    data = []
    for new in temp:
        if len(data) == 0:
            pass
        elif len(data) and (new[0] - data[-1][0]) / data[-1][0] >= 0.01:
            new[-1] = 1
        elif len(data) and (new[0] - data[-1][0]) / data[-1][0] <= -0.01:
            new[-1] = 0
        else:
            new[-1] = 2
        data.append(new)

    data = pd.DataFrame(data, columns=['price', 'pe', 'pb', 'ps', 'eta', 'dar', 'flow', 'roe', 'target'],
                        dtype=float)
    target = data['target']
    target = target.astype('int')
    data = data.drop(columns='target')
    data = MinMaxScaler().fit_transform(data)
    data = np.array(data)
    target = np.array(target)
    if not os.path.exists(xgb_path):
        xgboost_stock(data, target, model, params, sqe_len, xgb_path)
    model = load(xgb_path)
    x = make_xgb_last_sqe(data, target, sqe_len)

    print('isnull', isnull)

    # plt_daily(day_price)
    # ply_financial(stock)
    # ply_indicator(stock_target)

    return model.predict_proba(x)[0]


def main(stock_name):
    if stock_name[0] == '6':
        stock_market = 'sh'
    else:
        stock_market = 'sz'
    if need_make_data(stock_name):
        make_data(stock_name, stock_market)
    price = list(predict_price(stock_name))
    print("price", price)
    _sell_or_buy = list(map(lambda x: float(x), list(sell_or_buy(stock_name))))
    # _sell_or_buy = [1, 1, 1]
    print("sell_or_buy", _sell_or_buy)
    return {
        'predict_price': float(price[0]),
        'rates': _sell_or_buy,
        'stock_info_path': f'{data_path}{stock_name}/stock_zh_a_daily.csv'
    }

if __name__ == '__main__':
    main('600893')
