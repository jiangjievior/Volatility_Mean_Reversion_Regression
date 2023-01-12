import numpy as np
import pandas as pd
import os
from 数据文件.基本参数 import *

#获取指定格式的截面数据
def get_cross_vol(
        path_vol=PATH_VOL_SAMPLE,
        num_date=757,#个股期权样本中包含的日期个数
):
    data = pd.read_csv(path_vol)

    # 每个股期权的交易个数,并筛选出符合适合数量的样本
    size_individual = pd.pivot_table(data, index='ticker', values='date', aggfunc=np.size)
    size_individual.sort_values(by='date', inplace=True, ascending=False)
    size_individual = size_individual[size_individual['date'] == num_date]

    data = data[data['ticker'].astype(str).apply(lambda x: x in size_individual.index)]
    vol_individual_pivot = pd.pivot_table(data, index=['date'], columns=['ticker'], values=['impl_volatility'])[
        'impl_volatility']
    vol_individual_pivot = vol_individual_pivot.T.dropna().T

    return vol_individual_pivot


#获得指定个股的时间序列数据
def get_series_vol(
    path_vol=PATH_VOL_SAMPLE,
    ticker='SPX',#待选择个股的代码
    ):
    data = pd.read_csv(path_vol)
    data=data[data['ticker']==ticker]
    return data






if __name__=='__main__':
    pass
































