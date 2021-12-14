import datetime
import os
import akshare as ak
import numpy as np

from stock.settings import BASE_DIR, STATIC_URL

STATIC_DIR = BASE_DIR + STATIC_URL + 'stock/'

def make_data(stock_name, stock_market):
    # 获取股票数据
    stock_zh_a_daily = ak.stock_zh_a_daily(symbol=stock_market + stock_name,  adjust="qfq")
    # 获取股票指标
    stock_a_lg_indicator = ak.stock_a_lg_indicator(stock=stock_name)
    stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(stock=stock_name)
    data_path = STATIC_DIR + stock_name + '/'
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    stock_zh_a_daily.to_csv(data_path + 'stock_zh_a_daily.csv')
    stock_a_lg_indicator.to_csv(data_path + 'stock_a_lg_indicator.csv')
    stock_financial_analysis_indicator_df.to_csv(data_path + 'stock_financial_analysis_indicator.csv')
    file = open(data_path + 'last_time.txt', 'w')
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')
    file.write(now_date)


def make_gru_last_sqe(data_raw, sqe_len):
    x = []
    for i in range(0, sqe_len):
        x.append(data_raw[-1 * sqe_len + i])
    x = np.array(x)
    x = np.reshape(x, (1, sqe_len, 7))
    return x


def make_xgb_last_sqe(data, target, sqe_len):
    x = [data[len(data) - sqe_len: len(data)]]
    x = np.array(x)
    x = x.reshape(x.shape[0], -1)
    return x
