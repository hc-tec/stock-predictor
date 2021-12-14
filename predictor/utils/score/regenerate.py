import pandas as pd
import tushare as ts
import datetime
import os
from .basepath import get


def get_target(code, filepath):
    real_code = ""
    if code[0] == '0' or code[0] == '3':
        real_code = code + '.SZ'
    else:
        real_code = code + '.SH'

    name = filepath + code + '.csv'
    # print(name)
    # print(real_code)

    return real_code, name


def get_code_list():
    code_list = []
    filename = get() + '\\code.txt'
    f = open(filename)
    contents = f.readlines()
    f.close()

    for content in contents:
        value = content.split('\n')
        code_list.append(value[0])

    return code_list


def regen(content="0"):
    if content == "0":
        print('Empty argument. Failed to regenerate data.')
        return

    content_list = ['lrb', 'cwzbsj', 'byhq', 'ggzjlx', 'mrzb', 'zcfz', 'yxhq']
    if content not in content_list:
        print("Invalid target. Regenerating data canceled.")
        return

    code_list = get_code_list()
    ts.set_token('f6b511d8d4529f19319e1861edadda749e64a5b8573102deec80cfd8')
    pro = ts.pro_api()

    # 全部更新
    if content == 'all':
        for i in content_list:
            filepath = get() + i + '\\'

            for code in code_list:
                real_code, path = get_target(code, filepath)
                df = pro.income(ts_code=real_code, start_date='20170101', end_date=datetime.datetime.now().strftime('%Y%m%d'),
                                fields='ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,basic_eps,diluted_eps,'
                                       'n_income,revenue')
                df.to_csv(path)

    filepath = get() + content + '\\'

    print("wtf happened?")

    for code in code_list:
        real_code, path = get_target(code, filepath)
        print(path)
        df = pro.income(ts_code=real_code, start_date='20170101', end_date=datetime.datetime.now().strftime('%Y%m%d'),
                        fields='ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,basic_eps,diluted_eps,'
                               'n_income,revenue')
        df.to_csv(path)
