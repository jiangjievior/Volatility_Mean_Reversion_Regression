import pandas as pd
import numpy as np
import os

from 数据文件.基本参数 import PATH_VOL_main

data=pd.read_csv(PATH_VOL_main,usecols=['date', 'days', 'delta', 'impl_volatility','cusip','ticker'])
data=data.loc[data['cusip']!='99999999',:]
# data=data.loc[data['cusip']!='99999999',:]





#
# data=data.loc[data['date']>=20170101,:]


# 每个股期权的交易个数,并筛选出符合适合数量的样本
size_individual = pd.pivot_table(data, index='cusip', values='date', aggfunc=np.size)
size_individual.sort_values(by='date', inplace=True, ascending=False)
size_individual=size_individual[size_individual>=360]
size_individual.dropna(inplace=True)

data = data[data['cusip'].astype(str).apply(lambda x: x in size_individual.index)]
vol_individual_pivot = pd.pivot_table(data, index=['date'], columns=['cusip'], values=['impl_volatility'])[
    'impl_volatility']
vol_individual_pivot = vol_individual_pivot.T.dropna().T


#逐年遍历每年的期权数据
data_last_year=None
year_start=1996
year_last=2021
for volatility_ in volatility:
    volatility_.columns

    if data_last_year is not None:
        volatility_=data_last_year.append(volatility_)
        volatility_.reset_index(inplace=True)

    year_end=str(volatility_.loc[len(volatility_)-1,'date'])[:4]
    years=np.arange(int(year_start),int(year_end))
    year_start=year_end
    data_last_year=volatility_.loc[volatility_['date'].astype(str).str[:4]==year_end,:]






















































