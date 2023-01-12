import numpy as np
import pandas as pd
import os
from 数据文件.基本参数 import *


data=pd.read_csv(PATH_VOL_SAMPLE)

data

#每个股期权的交易个数,并筛选出符合适合数量的样本
size_individual=pd.pivot_table(data,index='ticker',values='date',aggfunc=np.size)
size_individual.sort_values(by='date',inplace=True,ascending=False)
size_individual=size_individual[size_individual['date']==757]

data=data[data['ticker'].astype(str).apply(lambda x:x in size_individual.index)]
vol_individual_pivot=pd.pivot_table(data,index=['date'],columns=['ticker'],values=['impl_volatility'])['impl_volatility']
vol_individual_pivot=vol_individual_pivot.T.dropna().T







