from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

#获得过去n个交易日的标准差超出点
def value_over_std(
        surface:pd.DataFrame,#波动率曲面数据
        windows_std:int=200,#用于计算移动标准差的窗口长度
        num_std:int=3,#超过该个数的标准差，将视为异常点

):
    surface

    #计算移动标准差
    surface['std_windows']=surface['impl_volatility'].rolling(windows_std).std()
    surface['mean_windows'] = surface['impl_volatility'].rolling(windows_std).mean()
    #寻找高于均值K个标准差的值
    for K in [0.5,1,2]:
        surface[f'over_std_{K}']=(surface['impl_volatility']>=(surface['std_windows']+K*surface['mean_windows']))
        surface[f'over_std_{K}']=surface[f'over_std_{K}'].apply(lambda x:1 if x==True else np.nan)
        surface[f'value_over_std_{K}']=surface[f'over_std_{K}']*surface['impl_volatility']

    return surface







if __name__=='__main__':
    surface=pd.read_csv(PATH_VOL_SURFACE_SPX)
    surface_days_delta=surface[(surface['days']==30)&(surface['delta']==50)]
    surface_days_delta.index=range(len(surface_days_delta))
    surface_days_delta=value_over_std(surface_days_delta,windows_std=20,num_std=2)

    #绘图
    date_start=20160407
    date_end=20190809
    surface_days_delta_date=surface_days_delta[(surface_days_delta['date']>=date_start)&(surface_days_delta['date']<=date_end)]
    plt.figure(figsize=(24,8))
    #surface_days_delta_date.index=surface_days_delta_date['date'].astype(str)
    plt.plot(surface_days_delta_date['impl_volatility'])
    plt.scatter(x=surface_days_delta_date.index,y=surface_days_delta_date['value_over_std_1'],color='r',linewidths=0.5)
    plt.xticks(np.array(surface_days_delta_date.index)[[int(x) for x in np.linspace(0,len(surface_days_delta_date)-1,15)]])






























