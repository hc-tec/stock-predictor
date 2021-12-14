from .pre import *

## ================最终接口================ ##

# 计算 1盈利能力
# 参数: 代码
# 返回值: 数据, 排名百分比, 排名
def cal_ROE(code):
    data, score, rank = calculate_score(code, 'roe')
    score = np.around(score, decimals=4)
    data = np.around(data, decimals=4)
    return float(data), float(score), float(rank)


# 计算 3每股收益增长率
# 参数: 代码
# 返回值: 数据, 排名百分比, 排名
def cal_EP(code):
    data, score, rank = calculate_score(code, 'basic_eps_yoy')
    score = np.around(score, decimals=4)
    data = np.around(data, decimals=4)
    return float(data), float(score), float(rank)


# 计算 3市盈率
# 参数: 代码
# 返回值: 数据, 排名百分比, 排名
def cal_PE(code):
    data, score, rank = calculate_score(code, 'pe')
    # calculate_score(code, 'pe')
    score = np.around(score, decimals=4)
    data = np.around(data, decimals=4)
    return float(data), float(score), float(rank)


# 计算 4财务状况 流动资产与流动负债之比
# 参数: 代码
# 返回值: 数据, 排名百分比, 排名
def cal_AL(code):
    data, score, rank = calculate_assets_liab(code)
    score = np.around(score, decimals=4)
    data = np.around(data, decimals=4)
    return float(data), float(score), float(rank)


# 计算 1个月的平均成本（不知道怎么用）
# 参数: 代码
# 返回值: 平均成本
def cal_avg_amt(code):
    target = 'month_amount'

    try:
        df = pd.read_csv(get_filepath('table') + target + '.csv', converters={u'ts_code': str})
    except FileNotFoundError:
        recollect_assets_liab()
        df = pd.read_csv(get_filepath('table') + target + '.csv', converters={u'ts_code': str})

    rank = np.where(df.ts_code == code)[0][0]
    rank += 1
    avg_amount = df.loc[rank - 1, target]

    target = 'month_vol'

    try:
        df = pd.read_csv(get_filepath('table') + target + '.csv', converters={u'ts_code': str})
    except FileNotFoundError:
        recollect_assets_liab()
        df = pd.read_csv(get_filepath('table') + target + '.csv', converters={u'ts_code': str})

    avg_vol = df.loc[rank - 1, 'month_vol']
    avg = avg_amount / avg_vol

    ts.set_token('f6b511d8d4529f19319e1861edadda749e64a5b8573102deec80cfd8')
    pro = ts.pro_api()

    real_code = ""
    if code[0] == '0' or code[0] == '3':
        real_code = code + '.SZ'
    else:
        real_code = code + '.SH'

    data = pro.monthly(ts_code=real_code, start_date='20200101', end_date=datetime.datetime.now().strftime('%Y%m%d'),
                       fields='amount, vol')
    amount = data.loc[0, 'amount']
    vol = data.loc[0, 'vol']

    res = amount / vol

    #     return avg, res
    return res

# 计算 5pb 市净率（总市值/净资产)
# 参数: 代码
# 返回值: 数据, 排名百分比, 排名
def cal_PB(code):
    data, score, rank = calculate_score(code, 'pb')
    score = np.around(score, decimals=4)
    return float(data), float(score), float(rank)


# 计算 6 市盈率（TTM，亏损的PE为空）
# 参数: 代码
# 返回值: 数据, 排名百分比, 排名
def cal_PE_TTM(code):
    data, score, rank = calculate_score(code, 'pe_ttm')
    score = np.around(score, decimals=4)
    return float(data), float(score), float(rank)


if __name__ == '__main__':
    print(cal_PE('000001'))
    print(cal_AL('000786'))
    print(cal_EP('000001'))
    print(cal_ROE('688036'))
