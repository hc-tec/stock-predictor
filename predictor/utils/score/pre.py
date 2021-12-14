import pandas as pd
import tushare as ts
import numpy as np
import os
import math
import datetime
from .basepath import get
from .regenerate import get_code_list


# 获取目录下所有文件名
def get_all_code(filepath):
    code_list = []
    for root, dirs, files in os.walk(filepath):
        for f in files:
            code_list.append(f)
    return code_list


# 根据指标名, 查找相应的路径
# 参数：指标名称
def get_filepath(target):
    # 财务指标数据
    list_1 = ['profit_to_gr', 'current_ratio', 'eps', 'assets_turn', 'inv_turn', 'ar_turn', 'roe', 'basic_eps_yoy']
    if target in list_1:
        return get() + '\\cwzbsj\\'

    # 利润表
    list_2 = ['n_income', 'revenue']
    if target in list_2:
        return get() + '\\lrb\\'

    # 备用行情
    list_3 = ['avg_price']
    if target in list_3:
        return get() + '\\byhq\\'

    # 个股资金流向
    list_4 = ['net_mf_amount', 'net_mf_vol']
    if target in list_4:
        return get() + '\\ggzjlx\\'

    # 每日指标
    list_5 = ['pe', 'pb', 'pe_ttm']
    if target in list_5:
        return get() + '\\mrzb\\'

    # 资产负债
    list_6 = ['total_cur_liab', 'total_cur_assets']
    if target in list_6:
        return get() + '\\zcfz\\'

    # 月线行情
    list_7 = ['month_close', 'month_open', 'month_vol', 'month_amount']
    if target in list_7:
        return get() + '\\yxhq\\'

    # 日线行情
    list_8 = ['close', 'open', 'vol', 'amount']
    if target in list_7:
        return get() + '\\yxhq\\'

    # 保存table
    if target == 'table':
        return get() + '\\table\\'

# 2021-02-26
# 获取单个指标的平均值.
# 参数: 股票代码文件名(*.csv), 指标, 取前count行
def single_avg(code, target, date=0):
    df = pd.read_csv(get_filepath(target) + code)
    if date == 0:
        res = df[target].mean()
    else:
        df['end_date'] = pd.to_datetime(df['end_date'], format='%Y%m%d')
        df = df[df['end_date'] > date]
        res = df[target].mean()

    del df

    if math.isnan(res):
        return 0

    return res


# 获取所有股票该指标的平均值.
# 参数: 指标
def all_avg(target):
    filepath = get_filepath(target)
    code_list = get_all_code(filepath)

    total = 0

    for code in code_list:
        total += single_avg(code, target)

    total /= len(code_list)

    return total


# 2021-02-22
# 统计所有股票: 取该股票某个指标的均值, 生成一张表
# 参数: 指标， 取前count位
def recollect_data(target, date=0):
    filepath = get_filepath(target)
    code_list = get_all_code(filepath)

    df_merge = pd.DataFrame(columns=['ts_code', target])

    for code in code_list:
        value = code.split('.')
        ts_code = value[0]
        df_merge = df_merge.append([{
            'ts_code': value[0],
            target: single_avg(code, target, date),
        }], ignore_index=True)

    df_merge = df_merge.sort_values(by=target, ascending=False)

    df_merge.to_csv(get_filepath('table') + target + '.csv', index=False)

    return df_merge


# 2021-02-27
# 统计所有股票的 流动负债/资产，进行比值，生成一张表
def recollect_assets_liab():
    target1 = 'total_cur_assets'
    target2 = 'total_cur_liab'

    filepath = get_filepath('total_cur_assets')
    code_list = get_all_code(filepath)

    col_name = 'assets_liab_ratio'

    df_merge = pd.DataFrame(columns=['ts_code', col_name])

    for code in code_list:
        value = code.split('.')
        ts_code = value[0]
        res_assets = single_avg(code, target1)
        res_liab = single_avg(code, target2)
        #         print('[' + str(code) + ']' + str(res_assets))
        #         print('[' + str(code) + ']' + str(res_liab))
        ratio = 0

        if res_assets == 0 or res_liab == 0:
            ratio = 0
        else:
            ratio = res_assets / res_liab

        df_merge = df_merge.append([{
            'ts_code': value[0],
            col_name: ratio,
        }], ignore_index=True)

    df_merge = df_merge.sort_values(by=col_name, ascending=False)
    df_merge.to_csv(get_filepath('table') + col_name + '.csv', index=False)

    return df_merge


# 2021-02-22
# 根据某个指标数据, 来计算分数. 用于 recollect_data 方法中。
# 参数: 指标名称
def recollect_score(target):
    df = pd.read_csv(get_filepath('table') + target + '.csv', converters={u'ts_code': str})
    return df


# 2021-03-02
# 检测代码是否存在
# 参数：代码
# 返回值 T / F
def check_code(code):
    code_list = get_code_list()
    if code not in code_list:
        return False
    else:
        return True

# 2021-02-26
# 给某个股票的某个指标打分, 按照排位方式
# 参数: 代码, 指标, 排位表, 是否更新数据[T or F, date]
# 返回值: 数据, 排名百分比, 排名
def calculate_score(code, target, recollect=False):
    if not check_code(code):
        return 0, 2, 400

    if not recollect:
        pass
    elif recollect[0]:
        recollect_data(target, recollect[1])

    try:
        df = pd.read_csv(get_filepath('table') + target + '.csv', converters={u'ts_code': str})
    except FileNotFoundError:
        recollect_data(target, 0)
        df = pd.read_csv(get_filepath('table') + target + '.csv', converters={u'ts_code': str})

    rank = np.where(df.ts_code == code)[0][0]
    rank += 1
    rate = rank / 300
    data = df.loc[rank - 1, target]

    return data, rate, rank


# 2020-02-27
# 给某个股票的 资产与负债之比，按照排位打分
# 参数：代码，是否更新数据(只要填 True 或 False)
# 返回值：

def calculate_assets_liab(code, recollect=False):
    if not check_code(code):
        return 0, 2, 400

    if not recollect:
        pass
    elif recollect:
        recollect_assets_liab()

    target = 'assets_liab_ratio'
    try:
        df = pd.read_csv(get_filepath('table') + target + '.csv', converters={u'ts_code': str})
    except FileNotFoundError:
        recollect_assets_liab()
        df = pd.read_csv(get_filepath('table') + target + '.csv', converters={u'ts_code': str})

    rank = np.where(df.ts_code == code)[0][0]
    #     ratio = df[code][target]
    rank += 1
    rate = rank / 300
    data = df.loc[rank - 1, target]

    return data, rate, rank
